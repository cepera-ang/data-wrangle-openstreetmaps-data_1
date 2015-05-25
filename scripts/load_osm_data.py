#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ceper_000'

import xml.etree.ElementTree as ET
import pprint
import re


def load_data():
    # Let's load our file, count tags and do some cleaning
    # 1.
    #
    #
    #
    #
    #

    filename = "tyumen_russia.osm"
    pprint.pprint(count_tags(filename))
    pass


def count_tags(filename):
    # YOUR CODE HERE
    # Here we count all different tags
    tags = {}

    for (event, elem) in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1

    return tags


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        key = element.attrib['k']

        if lower.search(key):
            keys["lower"] += 1
        elif lower_colon.search(key):
            keys["lower_colon"] += 1
        elif problemchars.search(key):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


if __name__ == '__main__':
    load_data()
