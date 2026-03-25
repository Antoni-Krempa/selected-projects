from src import *
import pickle
from PIL import Image,ImageDraw
import cupy as cp
import numpy as np



def main():
    with open("cache.pkl", "rb") as f:
        target_gpu, points, canvas_gpu, mask_circle, w, h, idx_gpu, vals_gpu = pickle.load(f)

    image=Image.open(r"C:\Users\akrem\Desktop\FOTY INŻYNIERKA\kolczyk.jpg").convert("RGB") 
    new_size = (
    int(round(image.width * 2)),
    int(round(image.height * 2))) 
    image = image.resize(new_size, Image.BICUBIC) 
    image = image.convert('L') #zamiana na skalę szarości
    npImage=np.array(image)
    image_vector = npImage[mask_circle] #aplikacja maski
    target_gpu = cp.asarray(image_vector, dtype=cp.int32) #zmiana na cp.array

    num_of_lines = 3000 
    list_of_instructions = get_list_of_instructions(target_gpu, canvas_gpu, num_of_lines, idx_gpu, vals_gpu)

    #apisz list_of_instructions do osobnego pliku
    with open("instructions.pkl", "wb") as f:
        pickle.dump(list_of_instructions, f)
    
    print(list_of_instructions)
    new_list = []
    for i in points:
        new_list.append(tuple(x*4 for x in i ))


    draw_insturctions(list_of_instructions, new_list, 4*w, 4*h)

main()


