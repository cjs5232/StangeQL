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
from src.page import Page
from src.LRUReplace import LRUReplace


class PageBuffer:

    def __init__(self, bufferSize, pageSize):
        self.buffer = []

        for i in range(bufferSize):
            self.buffer[i] = Page(i, pageSize)

        self.replace = LRUReplace(self)
        self.pageMap = {}
        self.numPages = 0

    def __len__(self):
        return self.numPages

    def get_Buffer(self):
        return self.buffer

    def new_page(self):
        page = self.allocate_page()
        page.incr_pin()
        return page

    # TODO:
    def allocate_page(self):
        pass

    def get_page(self, page_id):
        for page in self.buffer:
            if page.index == page_id:
                return page

        pageLRU = self.replace.least_recently_used()

        if pageLRU.is_modified():
            self.write_page(page)

        return self.read_page(page_id)

    # TODO:
    def read_page(self, page):
        pass

    def unpin_page(self, page_id, is_modified):
        for page in self.buffer:
            if page.index == page_id:
                page.decr_pin()
                if is_modified:
                    page.modified = True
                if page.pinCount == 0:
                    self.replace.buffer.append(page)
                return True
        return False

    def flush_page(self, page_id):
        for page in self.buffer:
            if page.index == page_id:
                self.write_page(page)
                return True
        return False

    # called when the DB is closed
    def flush_pages(self, page_id):
        for page in self.buffer:
            self.write_page(page)

    # TODO:
    def write_page(self, page):
        pass

    def delete_page(self, page_id):
        for page in self.buffer:
            if page.index == page_id:
                if page.pinCount == 0:
                    self.deallocate_page(page)
                else:
                    return ValueError("Page isn't pinned")

    # TODO:
    def deallocate_page(self, page):
        pass


