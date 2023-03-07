"""
CSCI.421 - Database System Implementation

File: page.py
Description: Provides implementation for the page class with some basic functions for pinning and unpinning pages
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""


class Page:
    
    def __init__(self, id, table_num, attributes):
        self.id = id
        self.table_num = table_num
        self.attributes = attributes
        self.records = []
        self.pinCount = 0
        self.modified = False
        self.state = -1

    def incr_pin(self):
        self.pinCount += 1

    def decr_pin(self):
        self.pinCount -= 1

    def is_modified(self):
        return self.modified

    def get_pin(self):
        return self.pinCount

    def get_id(self):
        return self.id
    
    def get_page_records(self):
        return self.records