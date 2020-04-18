import cv2
import numpy as np
from fast_histogram import histogram2d


def calc_bgr(img):
    """Return the normalized b, g, r values of the given 'img' image.

    !Note the return order.

    Typical use:
        img = cv2.imread("image.png")
        b, g, r = calc_cgr(img)

    Calculation:
        R = R / (R + G + B)
        G = G / (R + G + B)
        B = B / (R + G + B)
    """
    img = img.astype(float)
    # Add a small number to the denominator to avoid 'ZeroDivisionError'.
    r = img[..., 2] / (img[..., 0] + img[..., 1] + img[..., 2] + 1e-6)
    g = img[..., 1] / (img[..., 0] + img[..., 1] + img[..., 2] + 1e-6)
    b = 1 - r - g
    return b, g, r


def calc_rg_hist(x, y, bin_):
    """Calculate the two-dimensional rg histogram with 'bin_' bin from the
    given 'x' and 'y' arrays.

    Typical use:
        img = cv2.imread("image.png")
        b, g, r = calc_bgr(img)
        calc_2d_rg_hist(r, g, bin_=256)
    """
    return histogram2d(y.ravel(), x.ravel(),
                       bins=[bin_, bin_], range=[[0, 1], [0, 1]])


def contrast_stretch(array, a1, a2):
    """Perform min-max constrast stretching on the given 'array' array.

    Typical use:
        # 1. Get rid of the brightest 5% of the values. 
        contrast_stretch(luminosity, a1=0, a2=.95)
        # 2. Get rid of the less brightest 20% of the values.
        contrast_stretch(luminosity, a1=.2, a2=1)
    """
    array_1D = np.sort(np.ravel(array))
    min_ = array_1D[int(a1 * array_1D.shape[0])]
    max_ = array_1D[int(a2 * array_1D.shape[0])]
    array[array < min_] = min_  # Handle underflow
    array[array > max_] = max_  # Handle overflow
    return array


def norm_array(array, range_):
    """Normalize the given 'array' array.
    The maximam value of the original array gets transformed to 'range_'.
    """
    max_ = array.max()
    if max_ > 0:
        array = (array.astype(float) / max_ * range_).astype(float)
    return array


def rg_color_space(size):
    """Generate a rectangular image with the given 'size' size.
    """
    img = np.zeros((size, size, 3), np.uint8)
    for row in range(size):
        for col in range(size):
            r = (col / size)
            g = (row / size)
            b = 1 - r - g
            # only interpreted if (y <= 1 -x)
            if (row <= size - col):
                img[row, col] = (b * 255, g * 255, r * 255)
    img = np.flipud(img)
    return img


def calc_img_rg_hist(img, size=256, a1=0, a2=0.9975):
    """Generate the two-dimensional rg histogram of the given 'img' image
    with 'size' size. 'a1' and 'a2' are the same as in 'contrast_stretch'.

    Typical use:
        img = cv2.imread("image.png")
        rg_img = calc_rg_hist(img, size=256)
        cv2.imshow(rg_img)
    """
    _, g, r = calc_bgr(img)
    rg = calc_rg_hist(r, g, size)
    rg = contrast_stretch(rg, a1, a2)
    rg = norm_array(rg, size)
    return np.flipud(rg)
