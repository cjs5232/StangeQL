"""
CSCI.421 - Database System Implementation

File: catalog.py
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""

import json
import io
import os

""" Nested dictionary"""
"""Gonna need some attributes like, name of DB, and attributes"""


def create_catalog():
    dict2 = {
        "name": "tab1",
        "attributes": [
            {
                "name": "att1",
                "type": "varchar(10)",
                "primary_key": False

            },
            {
                "name": "att2",
                "type": "char(20)",
                "primary_key": False

            }
        ]
    }
    dict3 = {
        "name": "tab2",
        "attributes": [
            {
                "name": "att3",
                "type": "test",
                "primary_key": False
            },
            {
                "name": "tab4",
                "type": "testAgain",
                "primary_key": False

            }
        ]
    }
    dictionary = {
        "db": {
            "name": "meatball",
            "location": "C:\\Users\\arcoo\\PycharmProjects\\DBMS-DSI-Project\\src",
            "page_size": 256,
            "buffer_size": 128
        },
        "tables": [
            dict2,
            dict3
        ]
    }
    with open("sample.json", "w") as outfile:
        json.dump(dictionary, outfile)

    dumped_json = json.dumps(dictionary)

    bytes_data = bytes(dumped_json, encoding='utf-8')

    # Open a binary file for writing
    with open("bintests", "wb") as write_file:
        # Write the bytes data to the binary file
        write_file.write(bytes_data)


def print_catalog(path):
    fileExist = os.path.exists(path)
    if not fileExist:
        print("No catalog file in path: " + path)
        return 1

    f = open('sample.json')
    data = json.load(f)

    for i in data["db"]:
        print(i, end=': ')
        print(data["db"][i])
    print()

    tableFlag = False
    for i in data["tables"]:
        tableFlag = True
        print("Table name: " + i["name"])
        for x in i["attributes"]:
            print(x)
        print()

    if not tableFlag:
        print("There are no tables to display")

    return 0

def print_table(table_name):
    f = open('sample.json')
    data = json.load(f)

    for i in data["tables"]:

        if i["name"] == table_name:
            print("Schema for Table: " + table_name)
            for x in i["attributes"]:
                print(x)
            f.close()
            return 0

    print("No such table " + table_name)
    f.close()
    return 1

def table_exists(table_name):
    f = open('sample.json')
    data = json.load(f)

    for i in data["tables"]:

        if i["name"] == table_name:
            f.close()
            return 0
    f.close()
    return 1

def table_attributes():
    return


create_catalog()
print_catalog('sample.json')