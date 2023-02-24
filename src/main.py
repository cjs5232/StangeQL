"""
CSCI.421 - Database System Implementation

File: main.py
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""
import sys
import os
import query_processor as qp
import catalog

class Driver:
    def __init__(self, args) -> None:
        self.args = args
        self.processArgs()
        self.handoff()

    """
    Process the passed sys.args from the command line and handle errors with bad commands
    Params: args (array) - List of command line arguments
    """
    def processArgs(self):
        self.dbloc = sys.argv[1]
        try:
            self.pageSize = eval(sys.argv[2])
            self.bufferSize = eval(sys.argv[3])
        except NameError as e:
            print("PageSize and BufferSize must both be valid integers")
            sys.exit(e)

        print(f"Welcome to JottQL\nLooking at {self.dbloc} for existing db....")
        cat = catalog.Catalog(self.dbloc, self.pageSize, self.bufferSize)

        if not os.path.exists(self.dbloc):
            print(f"No existing db found\nCreating new db at {self.dbloc}")
            os.mkdir(self.dbloc)
            # cat.add_table()
            # cat.print_catalog()
            cat.create_catalog()
            print(f"New db created successfully\nPage size: {self.pageSize}\nBuffer size: {self.bufferSize}")
            #TODO: Create pages and buffers with given the buffer size
        x = cat.table_attributes("tab3")
        print(f"cat.TableAttributes {x}")
    """
    Hand off program to the query processor for user input handling.
    TODO: Refactor after QP has been implemented to spit back error messages and exit gracefully (most likely includes backing up 
    or saving the DB before a sys.exit())
    """
    def handoff(self):
        QP = qp.QueryProcessor(self.dbloc, self.pageSize, self.bufferSize)
        returnCode = QP.main()
        print("\nSafely shutting down the database...")
        print("Purging page buffer...)")
        # TODO
        print("Saving catalog...")
        # TODO:
        print("\nExiting the database...")
        sys.exit(returnCode)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        d = Driver(sys.argv)
    else:
        print("usage:\n\tmain.py db_loc pageSize bufferSize")
        sys.exit(-1)
