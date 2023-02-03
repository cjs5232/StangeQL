"""
CSCI.421 - Database System Implementation

File: buffer_manager.py
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""

def get_disk_addr(block):
    # if (block not in buffer)
    #   if (buffer out of space)
    #       if (LRU block modified)
    #           block written back to disk
    #       remove LRU block from buffer
    #   allocate space in buffer for block
    # return (block_addr from buffer)