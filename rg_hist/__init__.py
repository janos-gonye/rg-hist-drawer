import cv2

from core import calc_img_rg_hist, rg_color_space
from gamma import gamma_decode
from utils import copy_luminosity

def draw_rg_hist(path_in, path_out=None, a1=0, a2=.9975, size=256, blur=9):
    img = cv2.imread(path_in)
    if img is None:
        raise ValueError(f"Image not found '{path_in}'")
    if not (0 <= a1 <= 1) or not (0 <= a2 <= 1):
        raise ValueError("'a1' and 'a2' must between the values '0' and '1'")
    if a1 >= a2:
        raise ValueError("'a1' can't be larger than 'a2' or equal to it")

    if path_out is None:
        path_out = 'hist_' + path_in

    img_rg = calc_img_rg_hist(img, size)
    rg_space = rg_color_space(size)
    img_rg = copy_luminosity(img_rg, rg_space)
    img_rg = cv2.blur(img_rg, (blur, blur))
    img_rg = gamma_decode(img_rg)
    cv2.imwrite(path_out, img_rg)
