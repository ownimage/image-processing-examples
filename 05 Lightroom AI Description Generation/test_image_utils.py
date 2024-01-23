import unittest

from image_util import get_image

jpg_path = 'sample\\parrots.jpg'
jpg_width = 768
nef_path = 'sample\\images\\DSC_3877.NEF'
nef_width = 7380


class TestStats(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_image_jpg(self):
        # GIVEN a jpg
        expected = jpg_width
        # WHEN
        img = get_image(jpg_path)
        actual = img.width
        # THEN
        assert actual == expected

    def test_get_image_nef(self):
        # GIVEN a nef
        expected = nef_width
        # WHEN
        img = get_image(nef_path)
        actual = img.width
        # THEN
        assert actual == expected

    def test_get_image_jpg_size(self):
        # GIVEN a nef
        expected = 500
        # WHEN
        img = get_image(jpg_path, 500)
        actual = img.width
        # THEN
        assert actual == expected

    def test_get_image_nef_size(self):
        # GIVEN a nef
        expected = 500
        # WHEN
        img = get_image(nef_path, 500)
        actual = img.width
        # THEN
        assert actual == expected


if __name__ == "__main__":
    unittest.main()  # run all tests
