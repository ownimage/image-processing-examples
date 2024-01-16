import unittest
from PIL import Image

from captioner import Captioner

test_filename = ('sample/parrots.jpg')
expected = [
    'this is a picture of two birds',
    'An image of two parrots',
    'Two colorful parrots sit close together on a tree branch, facing the camera and displaying their vibrant colors and unique features.',
    'IGNORE',
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
            assert expected[i] == actual[i], f'failed for {i}.\nexpected = ({expected[i]})\nactual = ({actual[i]})'

        test_image.close()
        file.close()
        print(captioner.get_stats())

if __name__ == "__main__":
    unittest.main()  # run all tests
