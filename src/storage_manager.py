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
        self.cat = catalog.Catalog(self.dbloc, self.pageSize, self.bufferSize)
        self.TYPE_LEN = 3
        self.INT_BYTE_MAX_LEN = 7
        self.INT_BYTE_TYPE = "big"


    #creates an empty table
    def create_table(self, table_name):
        filepath = self.dbloc + "/" + table_name + ".bin"
        #if there is not a table yet
        if os.path.exists(filepath):
            print(f"Table {table_name} already exists")
            return 1
        #create a new table
        f = open(filepath, "wb+")
        #write 0 as an integer to the table, there are currently 0 pages.
        #f.write(int.to_bytes(0, self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE))
        return 0

    def get_record(self, primary_key):

        return

    def get_page(self, table_number, page_number):
        return
    
    def bytes_to_int(self, byteRepresentation):
        return int.from_bytes(byteRepresentation, self.INT_BYTE_TYPE)

    #phase 1
    #returns a list of tuples ex: [(), (), ()][(), (), ()]
    def get_records(self, table_name):
        #get table attributes from catalog
        attributes = self.cat.table_attributes(table_name)
        records = []
        #TODO if filepath does not exist, throw an error
        filepath = self.dbloc + "/" + table_name + ".bin"
        #open the filepath
        with open(filepath, "rb") as f:
            #read in the number of pages
            num_pages = self.bytes_to_int(f.read(self.INT_BYTE_MAX_LEN))
            #for each page, read in the number of records, then read each record
            for i in range(num_pages):
                num_records = self.bytes_to_int(f.read(self.INT_BYTE_MAX_LEN))
                #for each record in the page, read each attribute
                for j in range(num_records):
                    record = []
                    #for each attribute in the record
                    for k in attributes:
                        attribute_type = k["type"]
                        print(attribute_type)
                        if attribute_type == 'integer':
                            value = self.bytes_to_int(f.read(self.INT_BYTE_MAX_LEN))
                        elif attribute_type == 'boolean':
                            value = self.bytes_to_int(f.read(1))
                            if value == 0:
                                record.append("False")
                            elif value == 1:
                                record.append("True")
                        elif attribute_type == 'double':
                            binfloatone = f.read(self.INT_BYTE_MAX_LEN)
                            floatone = int.from_bytes(binfloatone, self.INT_BYTE_TYPE)
                            binfloattwo = f.read(self.INT_BYTE_MAX_LEN)
                            floattwo = int.from_bytes(binfloattwo, self.INT_BYTE_TYPE)
                            value = float(str(floatone) + "." + str(floattwo))
                        #if fixed len char
                            #char_len = TODO get the length of the char in bytes
                                #this can be gotten from the attribute table from the catalog
                            #value = f.read(char_len)
                            #value = value.decode()
                        #if varchar
                            #knownInt = f.read(self.INT_BYTE_MAX_LEN)
                            #knownInt = int.from_bytes(knownInt, self.INT_BYTE_TYPE)
                            #print(knownInt)
                            #knownString = f.read(knownInt)
                            #print(knownString.decode())

                        #attribute_len = get_len()
                        #record.append(get_len())

                        #add the record attribute
                        record.append(value)
                    records.append(record)
            return records

    #helper function to get the length to read
    #attribute is the string of the current attribute being checked: ex)
    def get_len(attribute_type, value):
        return

    # phase 1
    def insert_record(self, table_name, attributes, values):
        print(len(values))
        if (len(attributes) != len(values)):
            print("SM: Attribute size does not equal value size")
            return 0

        filepath = self.dbloc + "/" + table_name + ".bin"
        #if there is not a table yet
        if os.path.exists(filepath) is False:
            print("SM: Table does not exist.")
            #create a new table
            #self.create_table(table_name)
            
        table_attributes = self.cat.table_attributes(table_name)
        #traverse the file to find where this record belongs
        #for each attribute in the table
        for i in range(len(table_attributes)):
            attribute = table_attributes[i]
            #if the attribute is the primary key, store the primary index for later
            if attribute["primary_key"]:
                primary_index = i
        #open the table file to read and write in binary
        with open(filepath, "rb+") as f:
            num_pages_pointer = f
            #read in the number of pages
            num_pages = self.bytes_to_int(f.read(self.INT_BYTE_MAX_LEN))
            #if there are 0 pages, create a new page
            if num_pages == 0:
                #increment num_pages to 1
                num_pages = 1
                #increment catalog page count
                self.cat.update_page_count(table_name,1)
                print(int.to_bytes(num_pages, self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE))
                #write page count to the table
                num_pages_pointer.write(int.to_bytes(num_pages, self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE))
                
            #for each page, read in the number of records, then read each record
            for i in range(num_pages):
                num_records_pointer = f
                num_records = self.bytes_to_int(f.read(self.INT_BYTE_MAX_LEN))
                #if there are 0 records, write the value.
                if num_records == 0:
                    num_records+=1
                    #write the number of records to the page
                    num_records_pointer.write(int.to_bytes(1, self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE))
                    print(values)
                    print(table_attributes)
                    #write a record to this position
                    f.write(self.record_to_bytes(values,table_attributes))
                    self.cat.update_record_count(table_name,1)
                    #return successfully wrote record
                    return 0
                #for each record in the page, read each attribute
                for j in range(num_records):
                    record = []
                    #for each attribute in the record
            #once the end of the file is reached, append new record
            

        return
    
    def record_to_bytes(self, values, attributes):
        for j in range(len(values)):
            print(len(attributes))
            for k in range(len(attributes)):
                attribute_type = attributes[k]["type"]
                print(attribute_type)
                if attribute_type == 'integer':
                    print(values[j][k])
                int_val = int.to_bytes(int(values[j][k]), self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE)
        return int_val
    
    def delete_record(self, primary_key):
        return

    def update_record(self, primary_key):
        return

if __name__ == '__main__':
    SM = StorageManager("testDB", "1024", "64")

    print(f"Exit Code: ")