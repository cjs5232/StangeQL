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
""" Nested dictionary"""
"""Gonna need some attributes like, name of DB, and attributes"""
def create_catalog():
    dict2 = {
                "name" : "tab1",
                "attributes" : [
                    {
                        "name" : "att1",
                        "type" : "varchar(10)"
                    },
                    {
                        "name" : "att2",
                        "type": "char(20)"
                    }
                ]
            }
    dictionary = {
        "db" : {
            "name" : "meatball",
            "location" : "C:\\Users\\arcoo\\PycharmProjects\\DBMS-DSI-Project\\src",
            "p_size" : 256,
            "b_size" : 128
        },
        "tables" : [
            dict2
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

def print_catalog():
    f = open('sample.json')
    data = json.load(f)
    """""
    for i in data["tables"]:
        print(data["tables"][i])
    """""
    print(data["tables"][0]["name"])


def print_schema(table_name):
    return

def table_attributes():
    return

create_catalog()
print_catalog()