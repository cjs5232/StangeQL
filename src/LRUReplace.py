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
        self.numBuffers = len(pageBuffer)
        self.buffer = pageBuffer.getBuffer()

        for dbloc in self.buffer:
            dbloc.state = -1  # available

        self.head = -1

    def insert(self, page):
        page.state = 0  # referenced

    def least_recently_used(self):
        if self.buffer:
            for i in range(2 * len(self.buffer)):
                self.head = (self.head + 1) % len(self.buffer)

                if self.buffer[self.head].state == 0:  # referenced
                    self.buffer[self.head].state = -1  # available

                elif self.buffer[self.head].state == -1:  # available:
                    return self.buffer[self.head]

        return None

    def erase(self, page):
        index = -1
        for dbloc in self.buffer:
            index += 1
            if dbloc.index == page.index:
                self.buffer.pop(index)
                return True
        return False

    def __len__(self):
        return self.numBuffers
