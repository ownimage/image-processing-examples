# https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
import logging
import xml.etree.ElementTree as ET
from copy import deepcopy

additional_namespace = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
}

__description_key = '{http://ns.adobe.com/photoshop/1.0/}CaptionWriter'


def __expect_one_in_list(single_list, name):
    o = __expect_one_or_none_in_list(single_list, name)
    if o is not None:
        return o
    raise Exception(f'{name} element not found.')


def __expect_one_or_none_in_list(single_list, name):
    if len(single_list) == 0:
        return None
    if len(single_list) == 1:
        return single_list[0]
    raise Exception(f'More than one {name} element found.')


def get_user_comment(tree):
    uc = None
    description = __get_Description(tree)
    if __description_key in description.attrib.keys():
        uc = description.attrib[__description_key]
    return uc


def __get_Description(tree):
    d = tree.findall('./rdf:RDF/rdf:Description', additional_namespace)
    return __expect_one_in_list(d, 'Description')


def replace_user_comment(tree, text):
    d = __get_Description(tree)
    d.attrib[__description_key] = text


def __register_all_namespaces(filename):
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])


def process(filename, text=""):
    __register_all_namespaces(filename)
    tree = ET.parse(filename)
    tree.write(filename)
    tree = ET.parse(filename)

    replace_user_comment(tree, text)
    ET.indent(tree, space=" ", level=0)
    tree.write(filename)
    return tree


