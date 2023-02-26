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
import page
import LRUReplace


class PageBuffer:

    def __init__(self, bufferSize, pageSize):
        self.buffer = []
        for i in range(bufferSize):
            self.buffer[i] = page(i)
        self.replace = LRUReplace(self)
        self.numPages = bufferSize/pageSize

    def __len__(self):
        return self.numPages

    def get_Buffer(self):
        return self.buffer

    def new_page(self, page_id):
        p = self.__init__(page_id)
        p.incr_pin()
        return p


    def get_page(self, p_id):
        for p in self.buffer:
            if p == p_id:
                return page
        # page not in buffer
        pageLRU = self.replace.least_recently_used()
        if pageLRU.is_modified():
            self.write_page(page)

        return self.read_page(p_id)

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


