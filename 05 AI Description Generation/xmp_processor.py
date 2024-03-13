# https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
import logging
import xml.etree.ElementTree as ET
from copy import deepcopy

'Originally LR_XML used the user_comment, it now uses the CaptionWriter'

__caption_writer_namespace = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
}

__user_comment_namespace = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'exif': 'http://ns.adobe.com/exif/1.0/'
}

__caption_writer_key = '{http://ns.adobe.com/photoshop/1.0/}CaptionWriter'


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


def get_caption_writer(tree):
    cw = None
    d = __get_description_element(tree)
    if __caption_writer_key in d.attrib.keys():
        cw = d.attrib[__caption_writer_key]
    return cw


def get_any_description(tree):
    d = get_caption_writer(tree)
    if d is not None:
        return d
    return get_user_comment(tree)


def get_user_comment(tree):
    elements = tree.findall('./rdf:RDF/rdf:Description/exif:UserComment', __user_comment_namespace)
    uc = __expect_one_or_none_in_list(elements, 'UserComment')
    if uc is None:
        return None

    alt = uc.find('rdf:Alt', __user_comment_namespace)
    if alt is None:
        return None

    li = alt.find('rdf:li', __user_comment_namespace)
    if li is None:
        return None

    return li.text


def __get_description_element(tree):
    d = tree.findall('./rdf:RDF/rdf:Description', __caption_writer_namespace)
    return __expect_one_in_list(d, 'Description')


def __replace_caption_writer(tree, text):
    d = __get_description_element(tree)
    d.attrib[__caption_writer_key] = text


def __register_all_namespaces(filename):
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])


def replace_description_in_file(filename, text=""):
    __register_all_namespaces(filename)
    tree = ET.parse(filename)
    tree.write(filename)
    tree = ET.parse(filename)

    __replace_caption_writer(tree, text)
    ET.indent(tree, space=" ", level=0)
    tree.write(filename)
    return tree


def __remove_user_comment(tree):
    d = __get_description_element(tree)
    ucs = d.findall('./exif:UserComment', __user_comment_namespace)
    for uc in ucs:
        d.remove(uc)


def upgrade(filename):
    'moves the user comment to the caption writer format'
    __register_all_namespaces(filename)
    tree = ET.parse(filename)
    uc = get_user_comment(tree)
    if uc is None:
        return
    cw = get_caption_writer(tree)
    tree.write(filename)

    text = uc if cw is None else f'{cw}\n\n{uc}'
    tree = ET.parse(filename)
    __remove_user_comment(tree)
    __replace_caption_writer(tree, text)
    ET.indent(tree, space=" ", level=0)
    tree.write(filename)
    return tree

def get_any_description_from_filename(filename):
    tree = ET.parse(filename)
    return get_any_description(tree)