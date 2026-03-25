from PIL import Image,ImageDraw
import numpy as np
import math
from skimage.draw import line
np.seterr(over='warn')


def draw_insturctions(instruction_list, points, w, h):
    
    prev_i = 0
    circle_image = Image.new("RGB", (w, h), (255, 255, 255))
    #zmieniamy go na obiekt typu draw
    draw = ImageDraw.Draw(circle_image)

    for ind,i in enumerate(instruction_list):
        if ind == 0:
            continue
        else:
            draw.line([points[prev_i], points[i]], fill=(0, 0, 0), width=1)
            prev_i = i

    npImageCircle=np.array(circle_image)
    Image.fromarray(npImageCircle).show()
    # Image.fromarray(npImageCircle).save("C:/Users/akrem/Desktop/Inżynierka/Images/2. 1000lines full~11.5min (zaszumione).png")  # zapis
 