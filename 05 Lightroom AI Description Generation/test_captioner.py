import unittest
import logging

from captioner import Captioner

test_filename = ('test/parrots.jpg')
expected = [
    'two parrots sitting on a branch',
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
        captioner = Captioner(logging.CRITICAL)
        actual = []
        # WHEN
        for i in range(Captioner.get_method_count()):
            if i == 3:
                actual.append('IGNORE')
            else:
                actual.append(captioner.describe(i, test_filename))
        # THEN
        for i in range(Captioner.get_method_count()):
            assert expected[i] == actual[i], f'failed for {i}.\nexpected = ({expected[i]})\nactual = ({actual[i]})'


if __name__ == "__main__":
    unittest.main()  # run all tests
