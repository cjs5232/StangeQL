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


    #phase 1
    def insert_records(self, table_name, records):
        """
        input records is a 2d array of records ex) [[12,"hello"],[5,"hey"]]


        NOTE:
            - Does storage manager do page splitting or page buffer?
            - How do we know table filename?
            - Where are we storing list/ordering of pages // free pages?
        """
        # Get table information from catalog
        catalog_tables = self.cat.get_catalog()["tables"]
        for table in catalog_tables:
            if table["name"] == table_name:
                table_info = table
                break

        # If there are no pages for this table
        if table_info["pageCount"] == 0:
            # make a new file for the table
            # add this entry to a new page
            # insert the page into the table file
            return 0 # end
        
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

    print(f"Exit Code: ")