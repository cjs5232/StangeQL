"""
CSCI.421 - Database System Implementation

File: page.py
Description: Provides implementation for the LRU which uses a circular queue algorithm to determine LRU
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""
from abc import ABC


class LRUReplace(ABC):

    def __init__(self, pageBuffer):
        super().__init__()
        self.bufferCount = len(pageBuffer)
        self.buffer = pageBuffer.getBuffer()
        for dbloc in self.buffer:
            dbloc.state = -1    # make everything in the buffer available

    def insert(self, page):
        page.state = 0  # referenced

    """
    loops through the buffer until finding an available page
    if none are available, the page that was added to the buffer first is returned
    """
    def least_recently_used(self):
        if self.buffer:
            # loop the buffer twice
            # first loop will only return available pages
            # second loop will only return referenced pages
            # pinned pages are protected from being removed
            for i in range(2 * self.bufferCount):
                index = i % self.bufferCount
                if self.buffer[index].state == -1:
                    return self.buffer[index]
                elif self.buffer[index].state == 0:
                    self.buffer[index].state = -1
        return None

    """
    remove a page from the buffer
    """
    def erase(self, page):
        index = -1
        # for each page
        for dbloc in self.buffer:
            index += 1
            # if the index of the page matches the one we are looking to remove
            if dbloc.index == page.index:
                # remove it from the buffer
                self.buffer.pop(index)
                return True
        return False

    def __len__(self):
        return self.numBuffers
