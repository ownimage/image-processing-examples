import os
import shutil
import unittest
import xml.etree.ElementTree as ET

from xmp_processor import process, get_user_comment

test_filename = 'in.xml'
test_comment = "THIS IS A COMMENT"
test_comment_2 = "THIS IS A DIFFERENT COMMENT"


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        remove(test_filename)

    def tearDown(self):
        remove(test_filename)

    def test_no_comment(self):
        # GIVEN
        shutil.copy('sample/no_comment.xml', test_filename)
        assert assert_no_comment(test_filename), 'input has comment when it should not'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment(test_filename) == test_comment, 'comment has not been added'

    def test_update_existing_comment(self):
        # GIVEN
        shutil.copy('sample/with_comment.xml', test_filename)
        exiting_comment = utility_get_user_comment(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment(test_filename) == test_comment, 'comment has not been added'

    def test_update_existing_comment_twice(self):
        # GIVEN
        shutil.copy('sample/with_comment.xml', test_filename)
        exiting_comment = utility_get_user_comment(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment(test_filename) == test_comment, 'comment has not been added'
        # WHEN
        process(test_filename, test_comment_2)
        # THEN
        assert utility_get_user_comment(test_filename) == test_comment_2, 'comment has not been added'

    def test_exiftool_generated_xmp_with_comment(self):
        # GIVEN
        shutil.copy('sample/xmp_from_dng_with_comment.xmp', test_filename)
        exiting_comment = utility_get_user_comment(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment(test_filename) == test_comment, 'comment has not been added'

    def test_exiftool_generated_xmp_with_no_comment(self):
        # GIVEN
        shutil.copy('sample/xmp_from_dng_without_comment.xmp', test_filename)
        assert assert_no_comment(test_filename), 'input has comment when it should not'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment(test_filename) == test_comment, 'comment has not been added'


def utility_get_user_comment(filename):
    tree = ET.parse(filename)
    rv = get_user_comment(tree)
    return rv


def assert_no_comment(filename):
    b = utility_get_user_comment(test_filename) is None
    return b


def remove(filename):
    try:
        os.remove(filename)
    except:
        pass


if __name__ == "__main__":
    unittest.main()  # run all tests
