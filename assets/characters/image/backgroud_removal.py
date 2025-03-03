# %%
import cv2
import numpy as np
from PIL import Image
from transparent_background import Remover
import os

# %%
remover = Remover()
all_imgs = [i for i in os.listdir("./") if i.endswith(".jpg")]
for i in all_imgs:
    img = Image.open(i).convert("RGB")
    out = remover.process(img, threshold=0.7)
    out.save(f'{i.split(".")[0]}.png')
