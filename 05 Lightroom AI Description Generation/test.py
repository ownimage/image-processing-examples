from captioner import Captioner
import logging

captioner = Captioner(logging_level = logging.INFO)
print(captioner.describe(0, 'new_image.jpg'))
print(captioner.describe(1, 'new_image.jpg'))
print(captioner.describe(2, 'new_image.jpg'))
print(captioner.describe(0, 'new_image.jpg'))
print(captioner.describe(1, 'new_image.jpg'))
print(captioner.describe(2, 'new_image.jpg'))