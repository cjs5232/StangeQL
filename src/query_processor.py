"""
CSCI.421 - Database System Implementation

File: query_processor.py
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""

class QueryProcessor:

    def __init__(self, dbloc, pageSize, bufferSize) -> None:
        self.dbloc = dbloc
        self.pageSize = pageSize
        self.bufferSize = bufferSize

    def create_table_cmd(self, query:list): #TODO
        
        return 1

    def select_cmd(self, attribute, tableName): #TODO
        # if table doesnt exist
        print("No such table foo")
        return 1 # implying error
        # else loop through table printing the selected attribute
            # if attribute = "*" print all
        # return 0  implying success

    def insert_cmd(self, query:list): #TODO
        return 1


    def display_schema_cmd(self, query:list): #TODO
        print(f"DB location: {self.dbloc}\nPage Size: {self.pageSize}\nBuffer Size: {self.bufferSize}\n")
        # if no tables
        print("No tables to display")
        # else loop through tables printing
        #   if fail return 1 implying ERROR
        return 0 # implying SUCCESS

    def display_info_cmd(self, tableName): #TODO
        tableSchema = "schema"
        tablePages = 0
        tableRecords = 0
        # if table exists
        print(f"Table name: {tableName}\nTable schema:\n\t{tableSchema}\nPages: {tablePages}\nRecords: {tableRecords}")
        # else return 1 implying ERROR
        return 0 #implying SUCCESS


    def help(self):
        """
        Print the help message to the user.
        """
        helpMsg = """Help
            - CREATE: This command will be used to create the schema for a table.
                    Structure: create table <name>(
                                <attr_name1> <attr_type1> primarykey,
                                <attr_name2> <attr_type2>,
                                ....
                                <attr_nameN> <attr_typeN>
                                );

                    Examples:
                        1. create table foo( num integer primarykey );
                        2. create table foo( age char(10),
                        num integer primarykey );
            
            - SELECT: This command will be used to access data in tables.
                    Structure: select * from <name>;
            
            - INSERT: This command will insert a new tuple into a table.
                    Structure: insert into <name> values <tuples>;

                    Examples:
                        1. insert into foo values (1 "foo" true 2.1);
                        2. insert into foo values (1 "foo bar" true 2.1),
                                                (3 "baz" true 4.14),
                                                (2 "bar" false 5.2),
                                                (5 "true" true null);
            
            - DISPLAY [
                    
                    - SCHEMA: This command will display the catalog of the database in an easy to read format.
                            Structure: display schema;

                    - INFO: This command will display the information about a table in an easy to read format.
                            Structure: display info <name>;
                    
                    ]"""
        print(helpMsg)
        return 0


    def process_input(self, query:list):
        """
        Process query. Depending on the command entered, call the 
        necessary function to execute the query and then return.
        Returns 0 if success and 1 if failure.
        """
        status = 0 # Default good status
        if query[0] == "help":
            return help()
        elif query[0] == "display":
            if query[1] == "schema":
                status = self.display_schema_cmd(query)
                return  status
            elif query[1] == "info":
                status = self.display_info_cmd(query[2])
                return  status
            else:
                return 1 # Return Failure
        elif query[0] == "select" and query[2] == "from":
            status = self.select_cmd(query[1], query[3])
            return status
        elif query[0] == "insert" and query[1] == "into":
            status = self.insert_cmd(query)
            return status
        elif query[0] == "create" and query[1] == "table":
            status = self.create_table_cmd(query)
            return  status
        
        status = 1 #Bad status
        return status

    def getUserInput(self):
        print("\nPlease enter commands, enter <quit> to shutdown the db\n")
        status = 0  # Good return
        while True:
            if not status == 0:
                return status

            readInput = input("JottQL> ")

            if readInput == "exit":
                return status

    def main(self):
        """
        Kick start main text processing loop (while loop) that awaits for a ; to end a statement or an exit command.
        NOTE: Carriage returns are ignored.

        Good status = 0
        Bad status = !0
        """
        print("\nPlease enter commands, enter <quit> to shutdown the db\n")

        blankString = ''

        while True:
            status = 0 
            readInput = input("JottQL> ").lower()
            if readInput == "<quit>":
                return status
            while not ";" in readInput:
                readInput += " " + input().lower()

            inputList = readInput.split(';')[0].split(" ")
            inputList = [input for input in inputList if input != blankString]
            print("INPUT LIST:", inputList) #TEMPORARY
            status = self.process_input(inputList)
            if status == 0:
                print("SUCCESS\n")
            else:
                print("ERROR\n")


if __name__ == '__main__':
    QP = QueryProcessor("testDB", "1024", "64")
    print(f"Exit Code: {QP.getUserInput()}")
