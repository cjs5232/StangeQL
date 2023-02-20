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
import codecs


""" Nested dictionary"""
"""Gonna need some attributes like, name of DB, and attributes"""
class Catalog:
    def __init__(self, location, page_size, buffer_size):
        self.location = location
        self.page_size = page_size
        self.buffer_size = buffer_size

    def create_catalog(self):
        dictionary = {
            "db": {
                "location": self.location,
                "page_size": self.page_size,
                "buffer_size": self.buffer_size
            },
            "tables": [
            ]
        }

        dumped_json = json.dumps(dictionary)

        bytes_data = bytes(dumped_json, encoding='utf-8')

        # Open a binary file for writing
        with open(self.location + "\\DBCatalog", "wb") as write_file:
            # Write the bytes data to the binary file
            write_file.write(bytes_data)


    def print_catalog(self):
        fileExist = os.path.exists(self.location + "\\DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(self.location + "\\DBCatalog")
        data = json.load(f)

        print("\nPrinting database information: ")
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

    def print_table(self, table_name):
        fileExist = os.path.exists(self.location + "\\DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(self.location + "\\DBCatalog")
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

    def table_exists(self, table_name):
        fileExist = os.path.exists(self.location + "\\DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(self.location + "\\DBCatalog")
        data = json.load(f)

        for i in data["tables"]:

            if i["name"] == table_name:
                f.close()
                return 0
        f.close()
        return 1

    def table_attributes(self, table_name, attribute_name):
        return


    def delete_table(self, table_name):
        fileExist = os.path.exists(self.location + "\\DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(self.location + "\\DBCatalog")
        data = json.load(f)

        for i in data["tables"]:

            if i["name"] == table_name:
                data["tables"].remove(i)
                dumped_json = json.dumps(data)
                bytes_data = bytes(dumped_json, encoding='utf-8')

                # Open a binary file for writing
                with open("sample.json", "wb") as write_file:
                    # Write the bytes data to the binary file
                    write_file.write(bytes_data)
                f.close()
                return 0

        print("Table - " + table_name + " not found in catalog")
        return 1

    def add_table(self):
        fileExist = os.path.exists(self.location + "\\DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(self.location + "\\DBCatalog")
        data = json.load(f)

        test_dict = {
            "name": "tab3",
            "attributes": [
                {
                    "name": "att5",
                    "type": "varchar(10)",
                    "primary_key": False

                },
                {
                    "name": "att6",
                    "type": "char(20)",
                    "primary_key": False

                }
            ]
        }

        data["tables"].append(test_dict)

        dumped_json = json.dumps(data)
        bytes_data = bytes(dumped_json, encoding='utf-8')

        # Open a binary file for writing
        with open(self.location + "\\DBCatalog", "wb") as write_file:
            # Write the bytes data to the binary file
            write_file.write(bytes_data)
        f.close()



    """
    add_table()
    delete_table("tab3")
    print_catalog('sample.json')
    """