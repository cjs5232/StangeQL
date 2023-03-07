"""
CSCI.421 - Database System Implementation

File: record.py
Description: TODO
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""

class Record: #TODO

    def __init__(self, table_num:int, page_id, record_values:list, encoded_values=[]):
        self.table_num = table_num
        self.page_id = page_id
        self.values = record_values
        self.encoded_values = encoded_values
        
