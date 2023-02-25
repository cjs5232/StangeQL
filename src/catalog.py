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
import fileinput
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
        with open(f"{self.location}/DBCatalog", "wb+") as write_file:
            # Write the bytes data to the binary file
            write_file.write(bytes_data)
        return 0


    """
    Might not need
    What if path is the same, but page and buffer sizes are different?
    """
    def load_catalog(self):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        self.location = data["db"]["location"]
        self.page_size = data["db"]["page_size"]
        self.buffer_size = data["db"]["buffer_size"]

        f.close()
        return self


    def delete_table(self, table_name):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        for i in data["tables"]:

            if i["name"] == table_name:
                data["tables"].remove(i)
                dumped_json = json.dumps(data)
                bytes_data = bytes(dumped_json, encoding='utf-8')

                # Open a binary file for writing
                with open(f"{self.location}/DBCatalog", "wb") as write_file:
                    # Write the bytes data to the binary file
                    write_file.write(bytes_data)
                f.close()
                return 0

        print("Table - " + table_name + " not found in catalog")
        return 1

    """
    Helper function to determine if a table exists or not
    Returns 1 if yes, 0 if no, 2 if no catalog file
    """
    def table_exists(self, table_name):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 2

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        for i in data["tables"]:

            if i["name"] == table_name:
                f.close()
                return 1
        f.close()
        return 0

    """
    Adds table to the catalog where the table is a dictionary in the form of
    {
    "name": "x",
    "pageCount": x,
    "recordCount": x,
    "attributes": [
        {
            "name": "x",
            "type": "x",
            "primary_key": bool

        },
        ...
        ]
    }
    """
    def add_table(self, table): #didn't have attributes but was sent attributes in query_processor
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        data["tables"].append(table)

        dumped_json = json.dumps(data)
        bytes_data = bytes(dumped_json, encoding='utf-8')

        # Open a binary file for writing
        with open(f"{self.location}/DBCatalog", "wb") as write_file:
            # Write the bytes data to the binary file
            write_file.write(bytes_data)
        f.close()
        return 0

    """
    Adds the record count - val -  of the given table name
    to the record count
    recordCount += val (deletions will be negative numbers)
    """
    def update_record_count(self, table_name, val):
        self.update_count(table_name, val, "recordCount")

    """
    Adds the page count - val -  of the given table name
    to the page count
    pageCount += val (deletions will be negative numbers)
    """
    def update_page_count(self, table_name, val):
        self.update_count(table_name, val, "pageCount")

    """
    I wanted to save some space but keep it easy so I made this function more generic
    for page/record updates
    """
    def update_count(self, table_name, val, type):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        for i in data["tables"]:
            if i["name"] == table_name:
                i[type] += val
                dumped_json = json.dumps(data)
                bytes_data = bytes(dumped_json, encoding='utf-8')
                with open(f"{self.location}/DBCatalog", "wb") as write_file:
                    # Write the bytes data to the binary file
                    write_file.write(bytes_data)
                f.close()
                return 0

        print("Table " + table_name + " not found")
        f.close()
        return 1

    def print_catalog(self):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
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
            print("Table Schema:")
            for x in i["attributes"]:
                if x["primary_key"] is True:
                    print("\t" + x["name"] + ":" + x["type"] + " primarykey")
                else:
                    print("\t" + x["name"] + ":" + x["type"])
            print("Pages: " + str(i["pageCount"]))
            print("Records: " + str(i["recordCount"]))
            print()

        if not tableFlag:
            print("There are no tables to display")

        f.close()
        return 0

    def print_table(self, table_name):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        for i in data["tables"]:

            if i["name"] == table_name:
                print("Table name: " + table_name)
                print("Table Schema:")
                for x in i["attributes"]:
                    if x["primary_key"] is True:
                        print("\t" + x["name"] + ":" + x["type"] + " primarykey")
                    else:
                        print("\t" + x["name"] + ":" + x["type"])
                print("Pages: " + str(i["pageCount"]))
                print("Records: " + str(i["recordCount"]))
                f.close()
                return 0

        print("No such table " + table_name)
        f.close()
        return 1

    """
    Helper function to get the type of an attribute in the catalog
    Returns 1 if there is no table/attribute name
    Returns the type if table/attribute names exists
    """
    def get_attribute_type(self, table_name, attribute_name):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:
                        f.close()
                        return x["type"]
                print("No attribute " + attribute_name + " in table " + table_name)
                return 1
        print("No table of name " + table_name)
        return 1

    """
    Helper function to determine if an attribute is a primary key
    Returns 1 if there is no table/attribute name
    Returns the bool: True if it is a prim key, False otherwise
    """
    def determine_attribute_key(self, table_name, attribute_name):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:
                        f.close()
                        return x["primary_key"]
                print("No attribute " + attribute_name + " in table " + table_name)
                return 1
        print("No table of name " + table_name)
        return 1

    """
    Returns a dictionary of the attributes in the form of
    name: att_name
    type: att_type
    primary_key: bool whether or not its a primary key
    """
    def table_attributes(self, table_name):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        for i in data["tables"]:
            if i["name"] == table_name:
                f.close()
                return i["attributes"]

        # Do we want this to return 1?
        return 1

    """
    Returns the entire catalog as a json
    """
    def get_catalog(self):
        fileExist = os.path.exists(f"{self.location}/DBCatalog")
        if not fileExist:
            print("No catalog file in path: " + self.location)
            return 1

        f = open(f"{self.location}/DBCatalog")
        data = json.load(f)

        return data

    """
    add_table()
    delete_table("tab3")
    print_catalog('sample.json')
    
    *This is how we want the dictionary to be setup*
    test_dict = {
    "name": "tab3",
    "pageCount": 1,
    "recordCount": 1,
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
    """