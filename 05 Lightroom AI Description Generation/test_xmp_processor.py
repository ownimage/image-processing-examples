import unittest
import os
import shutil

import xml.etree.ElementTree as ET
# from lxml import etree as ET

from xmp_processor import process, get_user_comment, additional_namespace

test_filename = 'in.xml'
test_comment = "THIS IS A COMMENT"
test_comment_2 = "THIS IS A DIFFERENT COMMENT"


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        remove(test_filename)

    def tearDown(self):
        # remove(test_filename)
        pass

    def test_no_comment(self):
        # GIVEN
        shutil.copy('sample/no_comment.xml', test_filename)
        assert assert_no_comment_block(test_filename), 'input has comment when it should not'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment_text(test_filename) == test_comment, 'comment has not been added'

    def test_update_existing_comment(self):
        # GIVEN
        shutil.copy('sample/with_comment.xml', test_filename)
        exiting_comment = utility_get_user_comment_text(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment_text(test_filename) == test_comment, 'comment has not been added'

    def test_update_existing_comment_twice(self):
        # GIVEN
        shutil.copy('sample/with_comment.xml', test_filename)
        exiting_comment = utility_get_user_comment_text(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment_text(test_filename) == test_comment, 'comment has not been added'
        # WHEN
        process(test_filename, test_comment_2)
        # THEN
        assert utility_get_user_comment_text(test_filename) == test_comment_2, 'comment has not been added'

    def test_exiftool_generated_xmp_with_comment(self):
        # GIVEN
        shutil.copy('sample/xmp_from_dng_with_comment.xmp', test_filename)
        exiting_comment = utility_get_user_comment_text(test_filename)
        assert exiting_comment != test_comment, 'existing_comment can not equal test_comment'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment_text(test_filename) == test_comment, 'comment has not been added'


    def test_exiftool_generated_xmp_with__no_comment(self):
        # GIVEN
        shutil.copy('sample/xmp_from_dng_without_comment.xmp', test_filename)
        assert assert_no_comment_block(test_filename), 'input has comment when it should not'
        # WHEN
        process(test_filename, test_comment)
        # THEN
        assert utility_get_user_comment_text(test_filename) == test_comment, 'comment has not been added'

# tree = ET.parse(test_filename)
# n = tree.find('./rdf:RDF/rdf:Description', additional_namespace)
# print(n.attrib)


def utility_get_user_comment(filename, tree=None):
    if tree is None:
        tree = ET.parse(filename)

    return get_user_comment(tree)


def utility_get_user_comment_text(filename, tree=None):
    element = utility_get_user_comment(filename, tree)
    alt = element.find('rdf:Alt', additional_namespace)
    if alt is None:
        raise Exception('alt not found')
    li = alt.find('rdf:li', additional_namespace)
    if li is None:
        raise Exception('li not found')
    return li.text


def assert_no_comment_block(filename):
    return utility_get_user_comment(test_filename) is None


def remove(filename):
    try:
        os.remove(filename)
    except:
        pass


if __name__ == "__main__":
    unittest.main()  # run all tests
    # SimpleTestCase().test_update_existing_comment_twice()
