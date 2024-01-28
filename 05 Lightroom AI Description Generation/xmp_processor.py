# https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
import logging
import xml.etree.ElementTree as ET

additional_namespace = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'exif':  'http://ns.adobe.com/exif/1.0/'
}


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
    es = tree.findall('./rdf:RDF/rdf:Description/exif:UserComment', additional_namespace)
    return __expect_one_or_none_in_list(es, 'UserComment')


def __get_Description(tree):
    d = tree.findall('./rdf:RDF/rdf:Description', additional_namespace)
    return __expect_one_in_list(d, 'Description')


def __get_or_create_user_comment(tree):
    user_comment = get_user_comment(tree)
    if user_comment is None:
        description = __get_Description(tree)
        user_comment = ET.SubElement(description, 'exif:UserComment')
    return user_comment


def __register_all_namespaces(filename):
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])


def __replace_user_comment(element, text):
    alt = element.find('rdf:Alt', additional_namespace)
    if alt is None:
        alt = ET.SubElement(element, 'rdf:Alt')
    li = alt.find('rdf:li', additional_namespace)
    if li is None:
        li = ET.SubElement(alt, 'rdf:li', {'xml:lang': 'x-default'})
    li.text = text


def process(filename, text):
    __register_all_namespaces(filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    user_comment = __get_or_create_user_comment(tree)
    __replace_user_comment(user_comment, text)
    ET.indent(tree, space=" ", level=0)
    tree.write(filename)
    print('########################### ' + filename + ' ############################ ')

