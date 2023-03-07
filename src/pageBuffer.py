"""
CSCI.421 - Database System Implementation

File: pageBuffer.py
Description: subsystem responsible for allocating buffer space in main memory
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""
import LRUReplace
from page import Page
from record import Record
import catalog
import os
import re


class PageBuffer:

    def __init__(self, bufferSize, pageSize, dbloc):
        self.INT_MAX_LEN = 4
        self.INT_BYTE_TYPE = "big"
        self.STRING_ENCODING = "utf-8"
        self.bufferSize = bufferSize
        self.pageSize = pageSize
        self.dbloc = dbloc
        # self.buffer = []
        # for i in range(bufferSize):
        #     self.buffer[i] = page(i)
        # self.replace = LRUReplace(self)
        # self.numPages = bufferSize/pageSize


    def encode_record(self, record_vals, attributes): # TODO boolean
        """
        Purpose:
            Encode all values in a record
        Input:
            record_vals: list of values belonging to a record (in order)
            attributes: list of attribute types for the table 1:1 with record_vals list
        Output:
            encoded_records: list of values belonging to a record that are encoded
        """
        encoded_record = []
        for i in range(len(record_vals)):
            if attributes[i] == "integer":
                encoded_val = self.encode_int(record_vals[i])
                encoded_record.append(encoded_val)
            elif "varchar" in attributes[i]:
                encoded_val = self.encode_str(record_vals[i])
                encoded_val_len = self.encode_int(len(encoded_val))
                encoded_record.append([encoded_val_len, encoded_val])
            elif "char" in attributes[i]:
                encoded_val = self.encode_str(record_vals[i])
                encoded_record.append(encoded_val)
            elif attributes[i] == "double":
                split_double = str(record_vals[i]).split(".")
                encoded_integer1 = self.encode_int(int(split_double[0]))
                encoded_integer2 = self.encode_int(int(split_double[1]))
                encoded_record.append([encoded_integer1, encoded_integer2])
            elif attributes[i] == "boolean":
                pass
            else:
                return 1
        
        return encoded_record

    def decode_record(self, record_vals, attributes): # TODO boolean
        """
        Purpose:
            Decode all values in a record
        Input:
            record_vals: list of encoded values belonging to a record (in order)
            attributes: list of attribute types for the table 1:1 with record_vals list
        Output:
            decoded_records: list of values belonging to a record that are decoded
        """
        decoded_record = []
        for i in range(len(record_vals)):
            if attributes[i] == "integer":
                decoded_val = self.decode_int(record_vals[i])
                decoded_record.append(decoded_val)
            elif "varchar" in attributes[i]:
                decoded_val = self.decode_str(record_vals[i][1])
                decoded_record.append(decoded_val)
            elif "char" in attributes[i]:
                decoded_val = self.decode_str(record_vals[i])
                decoded_record.append(decoded_val)
            elif attributes[i] == "double":
                decoded_int1 = self.decode_int(record_vals[i][0])
                decoded_int2 = self.decode_int(record_vals[i][1])
                decoded_double = float(f"{decoded_int1}.{decoded_int2}")
                decoded_record.append(decoded_double)
            elif attributes[i] == "boolean":
                pass
            else:
                return 1
        return decoded_record

    def encode_int(self, num):
        bytes_val = num.to_bytes(self.INT_MAX_LEN, self.INT_BYTE_TYPE)
        return bytes_val

    def decode_int(self, encoded_int):
        decoded_int = int.from_bytes(encoded_int, self.INT_BYTE_TYPE)
        return decoded_int

    def encode_str(self, string):
        bytes_data_array = bytearray(string, self.STRING_ENCODING)
        for index in range(len(bytes_data_array)):
            bytes_data_array[index] ^= 0b11111111
        bytes_data = bytes(bytes_data_array)
        return bytes_data

    def decode_str(self, encoded_str):
        print(encoded_str)
        bytes_array = bytearray(encoded_str)
        for index in range(len(bytes_array)):
            bytes_array[index] ^= 0b11111111
        string_data = bytes(bytes_array).decode(self.STRING_ENCODING)
        return string_data

    def encode_and_write_record(self, record:Record, page:Page, record_pos):
        """
        Purpose:
            Encode an entire record and write it to a page in the correct location
        Input:
            record: 
                A single record object
            page: 
                The page (object) that the record belongs to
            record_num: 
                The record position in the page.
                Ex: record_pos == 5, insert so this record is the 5th record (row) in the table
                    record_pos == 1, insert so this is the 1st record (row) in the table
        Output:
            total_record_length:
                The length of the record in the file. 
                Ex: Used to move pointer to the start position of the record to insert after it
        """
        total_record_length = 0
        filename = f"{page.table_num}.bin"
        print("Filename:", filename)
        
        encoded_record = self.encode_record(record.values, page.attributes)
        print("Encoded Record:", encoded_record)

        if not os.path.exists(self.dbloc + filename):
            f = open(self.dbloc + filename, "x")
            f.close()
        with open(self.dbloc + filename, 'ab+') as file:
            for i in encoded_record:
                file.seek(record_pos)
                if type(i) == list:
                    file.write(i[0])
                    file.write(i[1])
                else:
                    file.write(i)
                record_pos += len(i)
                total_record_length += len(i)

        return total_record_length
    
    def read_and_decode_record(self, page:Page, record_pos:int) -> Record: # TODO boolean
        """
        Purpose:
            Decode a specified single record from a page in table file
        Input:
            page: 
                Page object that the record belongs to
            record_pos: 
                The record position in the page.
                Ex: record_pos == 5, read the 5th record (row) in the page
                    record_pos == 1, read the 1st record (row) in the page
        Output:
            record: Record object with the decoded and encoded list of values stored
                    along with the table and page it belongs to.
        """
        encoded_record = []
        filename = f"{page.table_num}.bin"
        print("Filename:", filename)
        if not os.path.exists(self.dbloc + filename):
            print("Table file does not exist")
            return 1
        with open(self.dbloc + filename, "rb") as file:
            file.seek(record_pos)
            for attribute in page.attributes:
                if attribute == "integer":
                    encoded_val = file.read(self.INT_MAX_LEN)
                    encoded_record.append(encoded_val)
                elif "varchar" in attribute:
                    encoded_str_len = file.read(self.INT_MAX_LEN)
                    decoded_str_len = self.decode_int(encoded_str_len)
                    encoded_val = file.read(decoded_str_len)
                    encoded_record.append([encoded_str_len, encoded_val])
                elif "char" in attribute:
                    n = re.findall("\d+", attribute)
                    n = int(n[0])
                    encoded_str = file.read(n)
                    encoded_record.append(encoded_str)
                elif attribute == "double":
                    encoded_val1 = file.read(self.INT_MAX_LEN)
                    encoded_val2 = file.read(self.INT_MAX_LEN)
                    encoded_record.append([encoded_val1, encoded_val2])
                elif attribute == "boolean":
                    pass
                else:
                    return 1
        
        record = Record(page.table_num, page.id, self.decode_record(encoded_record, page.attributes), encoded_record)
        page.records.append(record)
        return record

    def get_record_position(self, page:Page, desired_insert_pos:int):
        """
        page: The page the record you are getting position for belongs to
        desired_insert_pos: where you want to insert the record. ex: if 3, then you want it to be the third record in the page
                                                                     if 1 then first record in page
        """
        # Get start of the page
        position = self.pageSize * page.id # Assumming page.id is page number
        record_count = 0

        if desired_insert_pos == 1:
            return position
        while record_count < desired_insert_pos - 1:
            cur_record = self.read_and_decode_record(page, position)
            encoded_values = cur_record.encoded_values
            for i in range(len(encoded_values)):
                if type(encoded_values[i]) == list and "varchar" in page.attributes[i]:
                    position += (self.decode_int(encoded_values[i][0]) + self.INT_MAX_LEN)
                elif type(encoded_values[i]) == list and page.attributes[i] == "double":
                    position += (self.INT_MAX_LEN + self.INT_MAX_LEN)
                else:
                    position += len(encoded_values[i])
            record_count += 1
        
        return position

    def load_page_from_file(self, page): #TODO
        """
        Purpose:
            Load a page object with all records from a specific page
        """
        # Get start of the page
        position = self.pageSize * page.id # Assumming page.id is page number
        print("Position:", position)
        while position < self.pageSize:
            record = self.read_and_decode_record(page, position)
            break
            # for i in len(page.attributes):

            
        return page

    def write_page_to_file(self, page): #TODO
        return

def main():
    ############################
    # SETUP
    ############################
    bufferSize = 64
    pageSize = 100
    db_loc = "temp\\"

    table_info = { # Table section from catalog
         "name":"foo",
         "pageCount":0,
         "recordCount":0,
         "table_num": 0,
         "attributes":[
            {
               "name": "text",
               "type": "varchar(5)",
               "primary_key": False
            },
            {
                "name": "num",
                "type": "integer",
                "primary_key": True
            }
         ]
      }
    
    pb = PageBuffer(bufferSize, pageSize, db_loc)
    
    table_num = table_info["table_num"]
    attributes = ["varchar(5)", "integer", "char(5)", "double"] # NOTE remember to test with double, boolean and char
    
    r0 = ["hey", 5, "hello", 3.4]
    r1 = ["bye", 8, "heart", 5.6]
    
    page0 = Page(0, table_num, attributes)
    record0 = Record(page0.table_num, page0.id, r0)
    record1 = Record(page0.table_num, page0.id, r1)
    page0.records.append(record0)
    page0.records.append(record1)

    ############################
    # INDIVIDUAL METHOD TESTS
    ############################
    print("-------------------------TEST CALLS-------------------------")
    # encoded_int = pb.encode_int(5)
    # print("Encoded number 5:", encoded_int)
    # decoded_int = pb.decode_int(encoded_int)
    # print("Decoded number 5:", decoded_int)

    # encoded_str = pb.encode_str("hello")
    # print("Encoded 'hello':", encoded_str)
    # decoded_str = pb.decode_str(encoded_str)
    # print("Decoded 'hello':", decoded_str)

    # encoded_record = pb.encode_record(record0.values, page0.attributes)
    # print("Encoded record:", encoded_record)
    # decoded_record = pb.decode_record(encoded_record, attributes)
    # print("Decoded record:", decoded_record)

    ############################
    # PROD TESTING
    ############################
    print("-------------------------PROD TESTING-------------------------")
    # Encode and write records in page0 to file
    # print("--ENCODING AND WRITING")
    # desired_record_pos = 1
    # record_pos = pb.get_record_position(page0, desired_record_pos)
    
    # for record in page0.records:
    #     print("Record Position:", record_pos)
    #     total_record_length = pb.encode_and_write_record(record, page0, record_pos)
    #     record_pos += total_record_length
    #     print("--")

    # print("--READING AND DECODING")
    # desired_record_pos = 2 # Second Record in page
    # record_pos = pb.get_record_position(page0, desired_record_pos)
    # decoded_record = pb.read_and_decode_record(page0, record_pos)
    # print("Get second Record read and decoded: ", decoded_record.values)

    # desired_record_pos = 1 # First record in page
    # record_pos = pb.get_record_position(page0, desired_record_pos)
    # decoded_record = pb.read_and_decode_record(page0, record_pos)
    # print("Get first Record read and decoded: ", decoded_record.values)

    print("--LOAD PAGE FROM FILE")
    page1 = Page(0, table_num, attributes) # Same page id just for testing empty records list
    print("Initial Length of page records list:", len(page1.records))
    pb.load_page_from_file(page1)
    print("After Length of page records list:", len(page1.records))
    for i in range(len(page1.records)):
        print(page1.records[i].values)
    print("--")

main()