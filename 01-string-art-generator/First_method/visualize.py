import pickle
from src import *

with open("instructions.pkl", "rb") as f:
    list_of_instructions = pickle.load(f)

with open("cache.pkl", "rb") as f:
    target_gpu, points, canvas_gpu, mask_circle, w, h, idx_gpu, vals_gpu = pickle.load(f)

print(list_of_instructions)
new_list = []
for i in points:
    new_list.append(tuple(x*4 for x in i ))


draw_insturctions(list_of_instructions, new_list, 4*w, 4*h)