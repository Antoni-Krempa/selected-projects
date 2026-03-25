from PIL import Image,ImageDraw
import numpy as np
import math
from skimage.draw import line
import cupy as cp
np.seterr(over='warn')




def set_up(path, w_times):

    # Otwieranie i resize
    image=Image.open(path).convert("RGB") 
    
    new_size = (
    int(round(image.width * w_times)),
    int(round(image.height * w_times)))
    image = image.resize(new_size, Image.BICUBIC)  
    
    # Zmierzenie wymiarów + promień i środek
    w, h = image.size
    center = (w // 2, h // 2)
    radius = min(center) - 10  # minimalny promień z lekkim marginesem

    # Zaznaczenie punktów na obwodzie
    points = []
    num_points = 200

    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        points.append((x, y))



    # Tworzenie maski koła
    Y, X = np.ogrid[:h, :w]
    distance_from_center = (X - center[0])**2 + (Y - center[1])**2
    mask_circle = distance_from_center <= radius**2

    # Stworzenie omaskowanego wektora oryginalnego zdjęcia
    image = image.convert('L')
    npImage=np.array(image)
    image_vector = npImage[mask_circle]
    target_gpu = cp.asarray(image_vector, dtype=cp.int32)

    # Tworzymy rzadką bazę linii
    baza_idx  = []
    baza_vals = []
    max_nnz   = 0

    for i in range(num_points):          # 200
        for j in range(num_points):      # 200
            idx, vals = sparsify(draw_all_lines_modeled(
                h, w,
                points[i][1], points[i][0],
                points[j][1], points[j][0], mask_circle)
            )
            baza_idx.append(idx)
            baza_vals.append(vals)
            max_nnz = max(max_nnz, len(idx))

    n_pairs = num_points * num_points  # 40 000
    idx_mat  = np.full((n_pairs, max_nnz), -1,  dtype=np.int32)
    vals_mat = np.zeros_like(idx_mat, dtype=np.int32)
    lens     = np.zeros(n_pairs, dtype=np.int32)

    for k, (idx, vals) in enumerate(zip(baza_idx, baza_vals)):
        L = len(idx)
        idx_mat[k, :L]  = idx
        vals_mat[k, :L] = vals
        lens[k]         = L

   
    idx_gpu  = cp.asarray(idx_mat).astype(cp.int32)   # shape (40000, max_nnz)
    vals_gpu = cp.asarray(vals_mat).astype(cp.int16)  # shape (40000, max_nnz)


    # Tworzymy pusty canvas
    circle_vector = np.full((h,w),255)
    circle_vector = circle_vector[mask_circle]
    canvas_gpu = cp.array(circle_vector).astype(cp.int16)

    return target_gpu, points, canvas_gpu, mask_circle, w, h, idx_gpu, vals_gpu


def draw_all_lines_modeled(h,w,row_start,col_start,row_end,col_end, mask_circle): 

    circle_vector = np.full((h,w),0)
    temp_vector = circle_vector.copy()

    for i in range(2):

        rr,cc = line(row_start+i,col_start,row_end+i,col_end)

        mask = rr < h
        rr = rr[mask]
        cc = cc[mask]

        if i > 0: #uwaga zmiany
            
            temp_vector[rr,cc] =  25
            
        else:
            temp_vector[rr,cc] = 50

        rr,cc = line(row_start-i,col_start,row_end-i,col_end)
        
        mask = rr >= 0
        rr = rr[mask]
        cc = cc[mask]
        
        if i > 0: #uwaga zmiany
            temp_vector[rr,cc] =  25
            
        else:
            temp_vector[rr,cc] = 50
            

    temp_vector = temp_vector[mask_circle] 

    return temp_vector


def sparsify(vector):
    idx = np.nonzero(vector)[0].astype(np.uint32)
    vals = vector[idx].astype(np.int32)  
    return idx, vals






    