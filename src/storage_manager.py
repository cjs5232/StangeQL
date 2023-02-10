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

# phase 1
def get_record(primary_key):
    return

def get_page(table_number, page_number):
    return

def get_records(table_number):
    return

# phase 1
def insert_record(table_number, record):
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
    #if there is not a table yet
    if os.path.exists('./tables/table_number') is False:
        #create a new table
        f = open('./tables/' + table_number, "w")
        #create a new page
        f.write(b'1')
        f.write(b'page1')
        #add the record to the empty page
        f.write(b'1')
        #add the record
        
    return

def delete_record(primary_key):
    return

def update_record(primary_key):
    return

