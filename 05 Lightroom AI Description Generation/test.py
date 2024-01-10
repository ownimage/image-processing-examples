from captioner import Captioner
import logging
from PIL import Image

captioner = Captioner(logging_level = logging.INFO)
file = open('new_image.jpg', 'rb')
image = Image.open(file)
image.thumbnail((image.width / 4, image.height / 4))
print(captioner.describe(0, image))
print(captioner.describe(1, image))
print(captioner.describe(2, image))
print(captioner.describe(0, image))
print(captioner.describe(1, image))
print(captioner.describe(2, image))
image.close()
file.close()