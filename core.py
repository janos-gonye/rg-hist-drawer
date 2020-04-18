import cv2
import numpy as np
import fash_histogram import histogram_2d


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
    return histogram_2d(y.ravel(), x.ravel(),
                        bins=[bin, bin], range=[[0, 1], [0, 1]])


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
