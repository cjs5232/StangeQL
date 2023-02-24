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
        self.binToType = {
            b'001': "<class 'int'>",
            b'010': "<class 'float'>", 
            b'011': "<class 'str'>", #Varchar and char will have to be str
            b'100': "<class 'bool'>"
        }


    #creates an empty table
    def create_table(self, table_name):
        filepath = self.dbloc + "/" + table_name + ".bin"
        #if there is not a table yet
        if os.path.exists(filepath):
            print(f"Table {table_name} already exists")
            return 0
        #create a new table
        f = open(filepath, "w")
        #TODO write 0 as an integer to the table, there are currently 0 pages.
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
        attributes = self.cat.table_attributes(self, table_name)

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
                        #if int
                            #value = f.read(self.INT_BYTE_MAX_LEN)
                            #value = int.from_bytes(value, self.INT_BYTE_TYPE)
                        #if bool
                            #value = f.read(1)
                            #value = int.from_bytes(value, INT_BYTE_TYPE)
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
                        #record.append(value)
                    records.append(record)
                    
            type = f.read(self.TYPE_LEN)
            print(type)
            print(self.binToType[type])
            knownInt = f.read(self.INT_BYTE_MAX_LEN)
            knownInt = int.from_bytes(knownInt, INT_BYTE_TYPE)
            print(knownInt)
            knownString = f.read(knownInt)
            print(knownString.decode())
        
        return

    #helper function to get the length to read
    #attribute is the string of the current attribute being checked: ex)
    def get_len(attribute_type, value):
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
        getCatTables = self.cat.get_catalog(self)
        tables = getCatTables["tables"]
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