import cv2


def copy_luminosity(img_grey, img_color):
    """Override the luminosity (HSV -> V) of the given
    'img_color' image with the same sized grey 'img_grey' image.
    """
    img_color = img_color.copy()
    img_grey = img_grey.copy()
    img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
    img_color[..., 2] = img_grey
    return cv2.cvtColor(img_color, cv2.COLOR_HSV2BGR)
