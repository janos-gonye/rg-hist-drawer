GAMMA_DECODE_EXPONENT = 2.2
GAMMA_ENCODE_EXPONENT = 1 / 2.2


def gamma_correct(img, exponent):
    return ((img.copy() / 255.0) ** exponent) * 255


def gamma_encode(img):
    return gamma_correct(img, exponent=GAMMA_ENCODE_EXPONENT)


def gamma_decode(img):
    return gamma_correct(img, exponent=GAMMA_DECODE_EXPONENT)
