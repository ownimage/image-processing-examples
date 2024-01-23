import rawpy
from PIL import Image


def get_image(image_path, size=0):
    if image_path.upper().endswith('.JPG') or image_path.upper().endswith('.JPEG'):
        img = __get_image_jpg(image_path)
    else:
        img = __get_image_raw(image_path)

    if size != 0:
        img.thumbnail((size, size))

    return img


def __get_image_jpg(image_path):
    with open(image_path, "rb") as f:
        img = Image.open(f)
        img.copy()
    return img


def __get_image_raw(image_path):
    raw = rawpy.imread(image_path)
    rgb = raw.postprocess()
    img = Image.fromarray(rgb)
    return img
