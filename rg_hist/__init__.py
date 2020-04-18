import os

import cv2

from rg_hist.core import calc_img_rg_hist, rg_color_space
from rg_hist.gamma import gamma_encode
from rg_hist.utils import copy_luminosity


def draw_rg_hist(path_in, path_out, a1=0, a2=.9975, size=256, blur=0):
    img = cv2.imread(path_in)
    img_rg = calc_img_rg_hist(img, size)
    rg_space = rg_color_space(size)
    img_rg = copy_luminosity(img_rg, rg_space)
    if blur > 0:
        img_rg = cv2.blur(img_rg, (blur, blur))
    img_rg = gamma_encode(img_rg)
    cv2.imwrite(path_out, img_rg)
