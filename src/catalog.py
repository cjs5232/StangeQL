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


class Catalog:
    def __init__(self, location, page_size, buffer_size):
        self.location = location
        self.page_size = page_size
        self.buffer_size = buffer_size
        self.filename = "DBCatalog.bin"

    @property
    def create_catalog(self):
        dictionary = {
            "db": {
                "location": self.location,
                "page_size": self.page_size,
                "buffer_size": self.buffer_size
                # if you need the filename, just get it from self.filename
            },
            "tables": [
            ]
        }

        dumped_json = json.dumps(dictionary)

        self.write_to_file(dumped_json)

        return 0

    
    def write_to_file(self, dumped_json):
        """
        Makes json into byte array, xor with a bitmap of all 1s, converts
        byte array into bytes, and stores the binary into the file
        """
        bytes_data_array = bytearray(dumped_json, 'utf-8')
        for index in range(len(bytes_data_array)):
            bytes_data_array[index] ^= 0b11111111

        bytes_data = bytes(bytes_data_array)
        # Open a binary file for writing
        with open(f"{self.location}/{self.filename}", "wb+") as write_file:
            # Write the bytes data to the binary file
            write_file.write(bytes_data)

        return

    
    def read_from_file(self):
        """
        Does the opposite of writing.
        Grabs binary data as an array, reverses the xor bitmap, read array as bytes
        translates bytes to a string, reads the string as a json and returns the json
        """
        fileExist = os.path.exists(f"{self.location}/{self.filename}")
        if not fileExist:
            print("No catalog file in path: " + self.location + "/DBCatalog.bin")
            return 1

        f = open(f"{self.location}/DBCatalog.bin", 'rb')

        bytes_data = f.read()

        bytes_data_array = bytearray(bytes_data)
        for index in range(len(bytes_data_array)):
            bytes_data_array[index] ^= 0b11111111
        string_data = bytes(bytes_data_array).decode("utf-8")
        json_data = json.loads(string_data)
        f.close()
        return json_data

    
    def load_catalog(self):
        """
        Might not need
        What if path is the same, but page and buffer sizes are different?
        """
        data = self.read_from_file()

        #Doesnt need to update location since its already looking there
        #self.location = data["db"]["location"]
        self.page_size = data["db"]["page_size"]
        self.buffer_size = data["db"]["buffer_size"]

        return self

    
    def delete_table(self, table_name):
        """
        This method is what we will use for drop table commands
        Removes all data associated with a specific table
        """
        data = self.read_from_file()

        for i in data["tables"]:

            if i["name"] == table_name:
                data["tables"].remove(i)
                dumped_json = json.dumps(data)

                self.write_to_file(dumped_json)
                return 0

        print("Table - " + table_name + " not found in catalog")
        return 1

    
    def alter_table_add(self, table_name, attribute):
        """
        Finds the attribute based off of table name
        Adds the given attribute to the table's list of attributes
        """
        data = self.read_from_file()
        for i in data["tables"]:
            if i["name"] == table_name:
                i["attributes"].append(attribute)
                dumped_json = json.dumps(data)
                self.write_to_file(dumped_json)
                return 0

        print("Table " + table_name + " not found")
        return 1

    
    def alter_table_delete(self, table_name, attribute_name):
        """
        Finds the attribute based off of table name/att name
        Deletes the given attribute from the table's list of attributes
        if the the names are equal
        """
        data = self.read_from_file()
        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:
                        i["attributes"].remove(x)
                        dumped_json = json.dumps(data)
                        self.write_to_file(dumped_json)
                        return 0
                print("No attribute " + attribute_name + " + found")
                return 1

        print("Table " + table_name + " not found")
        return 1

    def get_page_order(self, table_name):
        """
        Gets the page order, may need to refactor depending on what is needed
        """
        data = self.read_from_file()
        for i in data["tables"]:

            if i["name"] == table_name:
                return i["page_order"]

        print("Table " + table_name + " not found")
        return 1

    def table_exists(self, table_name):
        """
        Helper function to determine if a table exists or not
        Returns 1 if yes, 0 if no, 2 if no catalog file
        """
        data = self.read_from_file()

        for i in data["tables"]:

            if i["name"] == table_name:
                return 1
        return 0

    
    def add_table(self, table): # didn't have attributes but was sent attributes in query_processor
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
                "primarykey": bool

            },
            ...
            ]
        }
        """
        data = self.read_from_file()

        data["tables"].append(table)

        dumped_json = json.dumps(data)
        self.write_to_file(dumped_json)

        return 0

    
    def update_record_count(self, table_name, val):
        """
        Adds the record count - val -  of the given table name
        to the record count
        recordCount += val (deletions will be negative numbers)
        """
        self.update_count(table_name, val, "recordCount")

    
    def update_page_count(self, table_name, val):
        """
        Adds the page count - val -  of the given table name
        to the page count
        pageCount += val (deletions will be negative numbers)
        """
        self.update_count(table_name, val, "pageCount")

    
    def update_count(self, table_name, val,type):
        """
        I wanted to save some space but keep it easy so I made this function more generic
        for page/record updates
        """
        data = self.read_from_file()

        for i in data["tables"]:
            if i["name"] == table_name:
                i[type] += val
                dumped_json = json.dumps(data)
                self.write_to_file(dumped_json)

                return 0

        print("Table " + table_name + " not found")

        return 1


    def print_catalog(self):
        data = self.read_from_file()

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
                if x["primarykey"] is True:
                    print("\t" + x["name"] + ":" + x["type"] + " primarykey")
                else:
                    print("\t" + x["name"] + ":" + x["type"])
            print("Pages: " + str(i["pageCount"]))
            print("Records: " + str(i["recordCount"]))
            print()

        if not tableFlag:
            print("There are no tables to display")

        return 0


    def print_table(self, table_name):
        data = self.read_from_file()

        for i in data["tables"]:

            if i["name"] == table_name:
                print("Table name: " + table_name)
                print("Table Schema:")
                for x in i["attributes"]:
                    if x["primarykey"] is True:
                        print("\t" + x["name"] + ":" + x["type"] + " primarykey")
                    else:
                        print("\t" + x["name"] + ":" + x["type"])
                print("Pages: " + str(i["pageCount"]))
                print("Records: " + str(i["recordCount"]))

                return 0

        print("No such table " + table_name)

        return 1

    
    def get_attribute_type(self, table_name, attribute_name):
        """
        Helper function to get the type of an attribute in the catalog
        Returns 1 if there is no table/attribute name
        Returns the type if table/attribute names exists
        """
        data = self.read_from_file()

        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:

                        return x["type"]
                print("No attribute " + attribute_name + " in table " + table_name)
                return 1
        print("No table of name " + table_name)
        return 1

    
    def determine_attribute_key(self, table_name, attribute_name):
        """
        Helper function to determine if an attribute is a primary key
        Returns 1 if there is no table/attribute name
        Returns the bool: True if it is a prim key, False otherwise
        """
        data = self.read_from_file()

        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:

                        return x["primarykey"]
                print("No attribute " + attribute_name + " in table " + table_name)
                return 1
        print("No table of name " + table_name)
        return 1

    
    def get_att_unique(self, table_name, attribute_name):
        """
        Helper function to determine if an attribute is unique
        Returns 1 if there is no table/attribute name
        Returns the bool: True if it is unique, False otherwise
        """
        data = self.read_from_file()

        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:

                        return x["unique"]
                print("No attribute " + attribute_name + " in table " + table_name)
                return 1
        print("No table of name " + table_name)
        return 1

    
    def get_att_notnull(self, table_name, attribute_name):
        """
        Helper function to determine if an attribute is not null
        Returns 1 if there is no table/attribute name
        Returns the bool: True if it is not null, False otherwise
        """
        data = self.read_from_file()

        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:

                        return x["notnull"]
                print("No attribute " + attribute_name + " in table " + table_name)
                return 1
        print("No table of name " + table_name)
        return 1

    
    def get_att_default(self, table_name, attribute_name):
        """
        Helper function to get default value 
        Returns 1 if there is no table/attribute name
        Returns the bool: True if it is not null, False otherwise
        """
        data = self.read_from_file()

        for i in data["tables"]:
            if i["name"] == table_name:
                for x in i["attributes"]:
                    if x["name"] == attribute_name:

                        return x["default"]
                print("No attribute " + attribute_name + " in table " + table_name)
                return 1
        print("No table of name " + table_name)
        return 1


    def table_attributes(self, table_name):
        """
        Returns a dictionary of the attributes in the form of
        name: att_name
        type: att_type
        primarykey: bool whether or not its a primary key
        """
        data = self.read_from_file()

        for i in data["tables"]:
            if i["name"] == table_name:

                return i["attributes"]

        # Do we want this to return 1?
        return 1

    
    def get_catalog(self):
        """
        Returns the entire catalog as a json
        """
        data = self.read_from_file()

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
            "default": "memes!",
            "primarykey": False,
            "notnull": True,
            "unique": False

        },
        {
            "name": "att6",
            "type": "char(20)",
            "primarykey": False
            "notnull": True,
            "unique": False
        }
    ]
    }
    """