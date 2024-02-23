import unittest
from PIL import Image
import logging
import sys

from captioner import Captioner

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
test_filename = ('sample/parrots.jpg')
expected = [
    'this is a picture of two birds',
    'An image of two parrots',
    'Two colorful parrots sit close together on a tree branch, facing the camera and displaying their vibrant colors and unique features.',
    'IGNORE',
    'The image features two parrots standing next to each other in a forest. The '
    'parrots are positioned close to the camera, with one bird on the left side and the other on the right side of '
    'the image. Both birds have their mouths open, possibly vocalizing or communicating with each other. The forest '
    'setting provides a natural and serene environment for these beautiful birds.'
]


class TestCaptioner(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_describe(self):
        # GIVEN
        file = open(test_filename, 'rb')
        test_image = Image.open(file)
        captioner = Captioner()
        actual = []
        # WHEN
        for i in range(Captioner.get_method_count()):
            if i == 3:
                actual.append('IGNORE')
            else:
                actual.append(captioner.describe(i, test_image))

        # THEN
        for i in range(Captioner.get_method_count()):
            assert expected[i] == actual[i], f'failed for {i}.\nexpected = ({expected[i]})\n  actual = ({actual[i]})'

        test_image.close()
        file.close()
        print(captioner.get_stats())


if __name__ == "__main__":
    unittest.main()  # run all tests
