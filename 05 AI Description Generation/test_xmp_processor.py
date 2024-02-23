import os
import shutil
import unittest
import xml.etree.ElementTree as ET

from xmp_processor import replace_description_in_file, get_any_description, get_caption_writer, upgrade, get_user_comment

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
        replace_description_in_file(test_filename, test_comment)
        # THEN
        assert utility_get_caption_writer(test_filename) == test_comment, 'comment has not been added'

    def test_update_existing_comment(self):
        # GIVEN
        shutil.copy('sample/with_comment.xml', test_filename)
        exiting_comment = utility_get_caption_writer(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        replace_description_in_file(test_filename, test_comment)
        # THEN
        assert utility_get_caption_writer(test_filename) == test_comment, 'comment has not been added'

    def test_update_existing_comment_twice(self):
        # GIVEN
        shutil.copy('sample/with_comment.xml', test_filename)
        exiting_comment = utility_get_caption_writer(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        replace_description_in_file(test_filename, test_comment)
        # THEN
        assert utility_get_caption_writer(test_filename) == test_comment, 'comment has not been added'
        # WHEN
        replace_description_in_file(test_filename, test_comment_2)
        # THEN
        assert utility_get_caption_writer(test_filename) == test_comment_2, 'comment has not been added'

    def test_exiftool_generated_xmp_with_comment(self):
        # GIVEN
        shutil.copy('sample/xmp_from_dng_with_comment.xmp', test_filename)
        exiting_comment = utility_get_caption_writer(test_filename)
        assert exiting_comment != test_comment and exiting_comment is not None, 'existing_comment can not equal test_comment'
        # WHEN
        replace_description_in_file(test_filename, test_comment)
        # THEN
        assert utility_get_caption_writer(test_filename) == test_comment, 'comment has not been added'

    def test_exiftool_generated_xmp_with_no_comment(self):
        # GIVEN
        shutil.copy('sample/xmp_from_dng_without_comment.xmp', test_filename)
        assert assert_no_comment(test_filename), 'input has comment when it should not'
        # WHEN
        replace_description_in_file(test_filename, test_comment)
        # THEN
        assert utility_get_caption_writer(test_filename) == test_comment, 'comment has not been added'

    def test_can_read_caption_writer_using_get_any_description(self):
        # GIVEN
        shutil.copy('sample/xmp_from_dng_with_comment.xmp', test_filename)
        # WHEN
        actual = utility_get_any_description(test_filename)
        # THEN
        assert actual == 'from dng', 'comment not found'

    def test_can_read_description_using_get_any_description(self):
        # GIVEN
        shutil.copy('sample/xmp_with_user_comment.xmp', test_filename)
        # WHEN
        actual = utility_get_any_description(test_filename)
        # THEN
        assert actual == 'Some random comment', 'comment not found'

    def test_upgrade_works_empty_caption_writer(self):
        # GIVEN
        shutil.copy('sample/xmp_with_user_comment.xmp', test_filename)
        assert utility_get_caption_writer(test_filename) is None, 'caption writer should be none'
        # WHEN
        upgrade(test_filename)
        # THEN
        assert utility_get_caption_writer(test_filename) == 'Some random comment', 'caption writer not upgraded'
        assert utility_get_user_comment(test_filename) is None, 'UserComment has not been removed'

    def test_upgrade_works_with_caption_writer(self):
        # GIVEN
        shutil.copy('sample/xmp_with_user_comment.xmp', test_filename)
        replace_description_in_file(test_filename, test_comment)
        assert utility_get_caption_writer(test_filename) == test_comment, 'caption writer should be set'
        # WHEN
        upgrade(test_filename)
        # THEN
        assert utility_get_caption_writer(test_filename) == f'{test_comment}\n\nSome random comment', 'caption writer not upgraded'
        assert utility_get_user_comment(test_filename) is None, 'UserComment has not been removed'

def utility_get_caption_writer(filename):
    tree = ET.parse(filename)
    rv = get_caption_writer(tree)
    return rv

def utility_get_any_description(filename):
    tree = ET.parse(filename)
    rv = get_any_description(tree)
    return rv

def utility_get_user_comment(filename):
    tree = ET.parse(filename)
    rv = get_user_comment(tree)
    return rv

def assert_no_comment(filename):
    b = utility_get_caption_writer(test_filename) is None
    return b


def remove(filename):
    try:
        os.remove(filename)
    except:
        pass


if __name__ == "__main__":
    unittest.main()  # run all tests
