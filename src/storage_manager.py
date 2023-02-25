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
            return 0
        #create a new table
        f = open(filepath, "wb+")
        #TODO write 0 as an integer to the table, there are currently 0 pages.
        f.write(int.to_bytes(0))
        return 1

    # phase 1
    def get_record(self, primary_key):
        """
        getCatTables = self.get_catalog(self)
        tables = getCatTables["tables"]
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
        """
        return

    def get_page(self, table_number, page_number):
        return
    
    def bytes_to_int(self, byteRepresentation):
        return int.from_bytes(byteRepresentation, self.INT_BYTE_TYPE)

    #phase 1
    #returns a list of tuples ex: [(), (), ()][(), (), ()]
    def get_records(self, table_name):
        attributes = self.cat.table_attributes(table_name)

        #get types of each attribute
        data_types = []
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
                        #if bool
                            #value = self.bytes_to_int(f.read(1))
                            #match value
                                #case 0:
                                    #record.append("False")
                                #case 1:
                                    #record.append("True")
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
                        #if double
                            #binfloatone = f.read(self.INT_BYTE_MAX_LEN)
                            #floatone = int.from_bytes(binfloatone, self.INT_BYTE_TYPE)
                            #binfloattwo = f.read(self.INT_BYTE_MAX_LEN)
                            #floattwo = int.from_bytes(binfloattwo, self.INT_BYTE_TYPE)
                            #value = float(str(floatone) + "." + str(floattwo))
                            #
                        
                        #attribute_len = get_len()
                        #record.append(get_len())

                        #add the record attribute
                        record.append(value)
                    records.append(record)
            return records
        return 1

    #helper function to get the length to read
    #attribute is the string of the current attribute being checked: ex)
    def get_len(attribute_type, value):
        return

    # phase 1
    #attributes is a dictionary holding attributes of each in the form (name, type) if key=primarykey value=column name
    def insert_record(self, table_name, attributes, values):
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
            #add this attribute's data type using a helper function that parses the attribute type from the catalog
            ####attribute_type = self.get_dtype(attribute["type"])
            #append this to the data types list
            ####data_types.append(attribute_type)
        #open the table file to read and write in binary
        with open(filepath, "rb+") as f:
            #read in the number of pages
            num_pages = self.bytes_to_int(f.read(self.INT_BYTE_MAX_LEN))
            #if there are 0 pages, create a new page
            if num_pages == 0:
                #increment catalog page count
                self.cat.update_page_count(table_name,1)
                #write page count to the table
                f.write(int.to_bytes(1, self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE))
                #increment num_pages to 1
                num_pages = 1
            
            #for each page, read in the number of records, then read each record
            for i in range(num_pages):
                num_records = self.bytes_to_int(f.read(self.INT_BYTE_MAX_LEN))
                #if there are 0 records, write the value.
                if num_records == 0:
                    #write the number of records to the page
                    f.write(int.to_bytes(1, self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE))
                    print(values)
                    print(table_attributes)
                    #write a record to this position
                    self.write_record(f,values,table_attributes)
                    self.cat.update_record_count(table_name,1)
                    #return successfully wrote record
                    return 0
                #for each record in the page, read each attribute
                #for j in range(num_records):
                 #   record = []
                    #for each attribute in the record
            #once the end of the file is reached, append new record
            

        return
    
    def write_record(self, position, values, attributes):
        for j in range(len(values)):
            for k in range(len(attributes)):
                attribute_type = attributes[k]["type"]
                print(attribute_type)
                if attribute_type == 'integer':
                    print(values[j][k])
                int_val = int.to_bytes(int(values[j][k]), self.INT_BYTE_MAX_LEN, self.INT_BYTE_TYPE)
                position.write(int_val)
        return 0

    def delete_record(self, primary_key):
        return

    def update_record(self, primary_key):
        return

if __name__ == '__main__':
    SM = StorageManager("testDB", "1024", "64")

    print(f"Exit Code: ")