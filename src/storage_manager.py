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


    def convert_record_types(self, record, attribute_types):
        """
        Input:
            record - [val, val, val, val], a single record / list of values
            attribute_types = [varchar(5), integer, ...], list of attribute types for table in order
        Returns:
            List of types for the given record. Primary use is for printing on errors and
            type checking against the table.
        """
        types = {"<class 'int'>": "integer", "<class 'float'>": "double", 
                 "<class 'bool'>": "boolean"}
        record_types = []
        
        count = 0
        for val in record:
            ugly_type = str(type(val))
            a_type = attribute_types[count]
            if ugly_type == "<class 'str'>":
                
                if "varchar" in a_type:
                    n = re.findall("\d+", a_type)
                    n = int(n[0])
                    if len(val) <= n:
                        new_type = a_type
                    else:
                        new_type = f"char({len(val)})"
                else:
                    new_type = f"char({len(val)})"
                record_types.append(new_type)
            else:
                record_types.append(types[ugly_type])
            count += 1
        return record_types


    def check_record_types(self, attributes, record):
        attribute_types = []
        for i in attributes:
            attribute_types.append(i["type"])
        record_types = self.convert_record_types(record, attribute_types)

        for i in range(len(record)):
            if record_types[i] == attribute_types[i]:
                continue
            else:
                print(f"row {tuple(record)}: Invalid data type: expected {tuple(attribute_types)} got {tuple(record_types)}")
                return 1
        return 0
    

    def check_primarykey(self, table_name, attributes, record): #TODO
        pk_index = None
        for i in range(len(attributes)):
            if attributes[i]["primary_key"] == True:
                pk_index = i
        new_pk_val = record[pk_index]
        print(new_pk_val)
        # Check current primary key values in the table to see if new_pk_val already exists
            # if it doesn't exist -- passes
            # If it does exist -- fails

        return


    #phase 1
    def insert_records(self, table_name, records):
        """
        input records is a 2d array of records ex) [[12,"hello"],[5,"hey"]]


        NOTE:
            - Does storage manager do page splitting or page buffer?
            - How do we know table filename?
            - Where are we storing list/ordering of pages // free pages?
        """
        table_filename = f"{table_name}.bin"
        # Get table information from catalog
        catalog_tables = self.cat.get_catalog()["tables"]
        for table in catalog_tables:
            if table["name"] == table_name:
                table_info = table
                break
        
        attributes = table_info['attributes']
        
        # Check record types against schema and if primary key exists
        for record in records:
            type_result = self.check_record_types(attributes, record)
            if type_result == 1:
                return 1
            pk_result = self.check_primarykey(table_name, attributes, record)
            if pk_result == 1:
                return 1
            

        # If there are no pages for this table
        if table_info["pageCount"] == 0:
            # --------- PSEUDO 1---------
            # make a new file for the table
            # add this entry to a new page
            # insert the page into the table file
            # --------- PLANNING 1---------
            """
            current_page = Make new page object
            for each record:
                if current_page is full
                    split and create new one
                    current_page = new page
                Make new record object
                append record object to page
            Create and open table file
                convert page(s) to binary
                write page(s) to the table file
            """
            return 0 # end
        # --------- PSEUDO 2---------
        # Read each table page in order from the table file:
            # iterate the records in page:
                # if the record belongs before the current record:
                    # insert the record before it
            # if the current page becomes overfull:
                # split the page
                # end
        # --------- PLANNING 2---------
        """
        table = open table file
        ...
        for page in table
            for new_record in records:
                for record in page
                    if new_record belongs before record
                        insert new_record before record
                if page becomes overfull
                    split page
                    end
        """
        # --------- PSEUDO 3---------
        # If the record does not get inserted:
            # insert it into the last page of the table file
            # if page becomes overfull:
                # split the page
            # end
        # --------- PLANNING 3---------
        """
        if record not inserted
            page = last page in table file
            insert record into page
            if page becomes overfull
                split page
            end
        """

        return 0
    
    #phase 1
    def get_page(self, table_name, page_number):
        #get from page buffer
        return

    #phase 1
    def get_all_records(self, table_name):
        return

    #phase 2
    def alter_table(self, table_name):
        return
    
    #phase 2
    def drop_table(self, table_name):
        return

    #phase 3
    def delete_record(self, table_name, primary_key):
        return

    #phase 3
    def update_record(self, table_name, primary_key):
        return
    


if __name__ == '__main__':
    SM = StorageManager("testDB", "1024", "64")
    records = [[12,"hello", "nooooo", 3.2, "n"],[5,"hey", "yuppp", 4.5, False]]
    attributes = [
                {
                    "name": "col1",
                    "type": "integer",
                    "primary_key": True
                },
                {
                    "name": "col2",
                    "type": "varchar(10)",
                    "primary_key": False
                },
                {
                    "name": "col3",
                    "type": "char(5)",
                    "primary_key": False
                },
                {
                    "name": "col4",
                    "type": "double",
                    "primary_key": False
                },
                {
                    "name": "col5",
                    "type": "boolean",
                    "primary_key": False
                }
            ]

    for record in records:
        # SM.check_record_types(attributes, record)
        SM.check_primarykey("foo", attributes, record)

    print(f"Exit Code: ")