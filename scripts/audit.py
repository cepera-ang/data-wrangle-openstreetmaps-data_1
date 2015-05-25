#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "..\\map_data\\tyumen_russia.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
# "Trail", "Parkway", "Commons"]
expected = ["улица", "переулок", "шоссе", "километр", "проезд", "тракт"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Rd.": "Road"
           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            # pprint.pprint(dict(street_types))


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_phone(elem):
    return (elem.attrib['k'] == "phone") or (elem.attrib['k'] == "contact:phone")


def is_website(elem):
    return elem.attrib['k'] == "website"


def is_postcode(elem):
    return elem.attrib['k'] == "addr:postcode"


def audit(osmfile):
    osm_file = open(osmfile, "r", encoding="utf-8")
    street_types = defaultdict(set)
    invalid_postcodes = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_phone(tag):
                    print(tag.attrib['v'], "\t", update_phone(tag.attrib['v']))
                elif is_website(tag):
                    print(tag.attrib['v'], "\t", update_website(tag.attrib['v']))
                elif is_postcode(tag):
                    temp_postcode = update_postcode(tag.attrib['v'])
                    if temp_postcode != tag.attrib['v']:
                        invalid_postcodes.append(tag.attrib['v'])
    pprint.pprint(invalid_postcodes)
    return street_types


def update_name(name, mapping):
    # YOUR CODE HERE
    m = street_type_re.search(name)
    # print(m)
    if m:
        street_type = m.group()
        print(street_type)
        # name = name.replace(street_type, mapping[street_type])
    return name


def update_phone(old_phone):
    # this script is quick and dirty as it didn't check some corner cases and
    # only work fine for particular dataset, so don't expect much from it

    # remove all non-numeric symbols except +
    new_phone = re.sub("[^0-9\+]", "", old_phone)

    # for local city phones we want to have format as such: +7(3452)12-34-56
    if new_phone.find("3452") != -1:  # ! here is a catch -- what if phone has 3452 not only in area code part?
        new_phone = new_phone.replace("3452", "(3452)")

        # check if we have leading +7 or not
        if new_phone.find("(3452)") == 0:
            new_phone = "+7" + new_phone

        # +7(3452)123456 -- number should be that way at this moment
        # +7(3452)12-34-56 -- final phone number
        new_phone = new_phone[0:10] + "-" + new_phone[10:12] + "-" + new_phone[12:14]
        return new_phone
    if new_phone.find("+7") == -1 and new_phone.find(
            "7") == 0:  # another catch here -- what if we have just number starting from 7?
        new_phone = "+" + new_phone

    # other phones go in different format
    # so we have to change it from +7xxx1234567 to +7(xxx)123-45-67
    new_phone = new_phone[0:2] + "(" + new_phone[2:5] + ")" + new_phone[5:8] + "-" + new_phone[8:10] + "-" + new_phone[
                                                                                                             10:12]
    return new_phone


def update_website(old_website):
    new_website = old_website
    if old_website.find("http") == -1:
        new_website = 'http://' + old_website
    return new_website


def update_postcode(old_postcode):
    """

    :type old_postcode: str
    """
    new_postcode = old_postcode
    try:
        if int(old_postcode) < 625000 or int(old_postcode) > 997000:
            new_postcode = ""
    except:
        new_postcode = ""
    return new_postcode


def test():
    st_types = audit(OSMFILE)

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            # print(name, "=>", better_name)


if __name__ == '__main__':
    test()
