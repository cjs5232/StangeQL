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
        self.cat = catalog.Catalog(self.dbloc, self.pageSize, self.bufferSize)


    """
    • getting a record by primary key
    • getting a page by table and page number
    • getting all records for a given table number
    • inserting a record into a given table
    • deleting a record by primary key from a given table
    • updating a record by primary key in a given table
    """
    #phase 1
    #input records is a 2d array of records ex) [[12,"hello"],[5,"hey"]]
    def insert_records(self, records):
        # if there are no pages for this table:
        # make a new file for the table
        # add this entry to a new page
        # insert the page into the table file
        
        # end
        # Read each table page in order from the table file:
        # iterate the records in page:
        # if the record belongs before the current record:
        # insert the record before it
        # if the current page becomes overfull:
        # split the page
        # end
        # If the record does not get inserted:
        # insert it into the last page of the table file
        # if page becomes overfull:
        # split the page
        # end
        # splitting a page:
        # make a new page
        # remove half the items from the current page
        # add the items to the new page
        # insert the new page after the current page in the table

        return
    
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

    print(f"Exit Code: ")