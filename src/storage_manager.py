"""
CSCI.421 - Database System Implementation

File: storage_manager.py
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""
import os
import re
import catalog

class StorageManager:

    def __init__(self, dbloc, pageSize, bufferSize) -> None:
        self.dbloc = dbloc
        self.pageSize = pageSize
        self.bufferSize = bufferSize

    #creates an empty table
    def create_table(self, table_name):
        filepath = self.dbloc + "/" + table_name + ".bin"
        #if there is not a table yet
        if os.path.exists(filepath):
            print("Table already exists")
            return 0
        #create a new table
        f = open(filepath, "w")
        f.write(b"0</page>")
        return 1
    
    """
    #helper method to create a record from attributes
    def create_record(attributes, values):
        record = ""
        for name in attributes:
            match attributes[name]:
                case "integer":

        

        return
    """
    def get_dtype(self, attribute_string):
        """
        match attribute_string:
            case "integer":
                return int
            case "double":
                return float
        """
        if "char" in attribute_string:
            return (str,attribute_val)
        attribute_val = int(re.findall(r"\((\d+)\)","char(10)")[0])
        
        return 1

    def parse_record(record, primary_key, attributes):
        
        return


    # phase 1
    def get_record(self, primary_key):
        cat = catalog.get_catalog(self)
        tables = cat["tables"]
        for table in tables:
            filepath = self.dbloc + "/" + table["name"] + ".bin"
            data_types = []
            for i in range(len(table["attributes"])):
                attribute = table["attributes"][i]
                if attribute[primary_key]:
                    primary_index = i
                data_types[i] = self.get_dtype(attribute["type"])

            f = open(filepath, "rb")
            table_file = f.read()
            #splitting the file by pages
            table_file = f.split("</page>")
            num_pages = int(table_file[1])
            #going through each page in the table_file
            for i in range(num_pages) - 1:
                records = table_file[i].split("</record>")
                for j in range(len(records)):
                    record = records[j].split(",")
                    if(primary_key == record[primary_index]):
                        return tuple(record)
        return 0

    def get_page(self, table_number, page_number):
        return

    def get_records(self, table_number):
        return

    # phase 1
    #attributes is a dictionary holding attributes of each in the form (name, type) if key=primarykey value=column name
    def insert_record(self, table_name, attributes, values):
        """
        if there are no pages for this table:
        make a new file for the table
        add this entry to a new page
        insert the page into the table file
        end
        3
        Read each table page in order from the table file:
        iterate the records in page:
        if the record belongs before the current record:
        insert the record before it
        if the current page becomes overfull:
        split the page
        end
        If the record does not get inserted:
        insert it into the last page of the table file
        if page becomes overfull:
        split the page
        end
        splitting a page:
        make a new page
        remove half the items from the current page
        add the items to the new page
        insert the new page after the current page in the table file
        """
        if (len(attributes) != len(values)):
            print("SM: Attribute size does not equal value size")
            return 0

        filepath = self.dbloc + "/" + table_name + ".bin"
        #if there is not a table yet
        if os.path.exists(filepath) is False:
            #create a new table
            f = open(filepath, "wb")
            #create a new page
            f.write(b"<numPages>1</numPages><page1><numRecords>1</numRecords>")
            #insert record being added
            for i in range(len(attributes)):
                f.write(b"")
            f.write(b"</page1>")
            return
        
        #if the table already exists, open the file
        f = open(filepath, "rw+")
        #traverse the file to find where this record belongs
        #check page length vs max page size
        cat = catalog.get_catalog(self)
        tables = cat["tables"]
        for table in tables:
            filepath = self.dbloc + "/" + table["name"] + ".bin"
            data_types = []
            for i in range(len(table["attributes"])):
                attribute = table["attributes"][i]
                if attribute["primary_key"]:
                    primary_index = i
                data_types[i] = self.get_dtype(attribute["type"])

            f = open(filepath, "rb")
            table_file = f.read()
            #splitting the file by pages
            table_file = f.split("</page>")
            num_pages = int(table_file[1])
            #going through each page in the table_file
            for i in range(num_pages) - 1:
                records = table_file[i].split("</record>")
                for j in range(len(records)):
                    records[j]

        return

    def delete_record(self, primary_key):
        return

    def update_record(self, primary_key):
        return

if __name__ == '__main__':
    SM = StorageManager("testDB", "1024", "64")
    print(f"Exit Code: ")