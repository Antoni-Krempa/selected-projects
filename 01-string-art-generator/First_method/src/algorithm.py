from PIL import Image,ImageDraw
import numpy as np
import math
from skimage.draw import line
import cupy as cp
np.seterr(over='warn')


def densify_window(
    idx_gpu:  cp.ndarray,     # (n_lines, max_nnz)  indeksy pikseli  (-1 = puste)
    vals_gpu: cp.ndarray,     # (n_lines, max_nnz)  odpowiadające wartości
    start_col: int,           # pierwszy wiersz-linia, 
    n_rows_out: int,          # liczba pikseli w masce 
    width: int = 200          # ile kolejnych linii od start_col
) -> cp.ndarray:

    # 1) Pobieramy odpowiedni blok linii (shape = width × max_nnz)
    rows      = slice(start_col, start_col + width)
    idx_block = idx_gpu[rows]           # (width, max_nnz)
    val_block = vals_gpu[rows]

    # 2) Maska prawdziwych wpisów (-1 = padding)
    mask = idx_block != -1
    row_local, pos = cp.nonzero(mask)   # row_local 0…width-1
    pix_idx   = idx_block[row_local, pos]
    val_local = val_block[row_local, pos]

    # 3) Składamy gęstą macierz (scatter)
    dense = cp.zeros((n_rows_out, width), dtype=vals_gpu.dtype)
    dense[pix_idx, row_local] = val_local
    return dense


def get_list_of_instructions(target_gpu, canvas_gpu, num_of_lines, idx_gpu, vals_gpu):

    batch_size = 100
    num_total = 200    
    num_batches = num_total // batch_size
    instruction_list = [0]
    last_best_point  = 0

    for i in range(num_of_lines):

        print(i)
        temp_vector = canvas_gpu.copy()
        best_error = 1e9
        best_idx_global = None
        best_vector = None

        for b in range(num_batches):
            start_col = last_best_point * 200 + b * batch_size

            # Wczytujemy tylko wycinek o batch_size kolumnach
            lines_batch = densify_window(idx_gpu, vals_gpu, start_col, target_gpu.size, batch_size)

            # Odejmujemy wektor i ustalamy różnicę z targetem
            added_batch = temp_vector[:, None] - lines_batch
            cp.maximum(added_batch, 0, out=added_batch)

            
            diff = target_gpu[:, None] - added_batch


            mse_batch = cp.mean(cp.square(diff), axis=0)  
            local_best_idx = int(cp.argmin(mse_batch).get())
            local_best_error = float(mse_batch[local_best_idx].get())

            if local_best_error < best_error:
                best_error = local_best_error
                best_idx_global = b * batch_size + local_best_idx
                best_vector = added_batch[:, local_best_idx].copy()

            # Oczyszczanie pamięci po batchu
            del lines_batch, added_batch, diff, mse_batch
            cp._default_memory_pool.free_all_blocks()

        last_best_point = best_idx_global
        instruction_list.append(best_idx_global)
        canvas_gpu = best_vector.copy()

    return instruction_list