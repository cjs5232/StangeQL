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
import re
import catalog
import os.path

class QueryProcessor:

    def __init__(self, dbloc, pageSize, bufferSize) -> None:
        self.dbloc = dbloc
        self.pageSize = pageSize
        self.bufferSize = bufferSize
        self.Catalog = catalog.Catalog(dbloc, pageSize, bufferSize)


    def checkDtype(self, dType):
        if "," in dType: dType = dType.rstrip(',')
        dataTypes = ['integer', 'double', 'boolean'] # 'char(n)', 'varchar(n)'
        if "varchar" in dType:
            n = re.findall("^varchar\(\d+\)$", dType)
            if len(n) == 1: 
                return 0
            else: 
                return 1
        elif "char" in dType:
            n = re.findall("^char\(\d+\)$", dType)
            if len(n) == 1: return 0
            else: return 1
        elif dType in dataTypes:
            return 0
        else:
            return 1


    def buildTableFile(self, tableName, attributes):
        filepath = self.dbloc + "/" + tableName + ".bin"
        if os.path.exists(filepath):
            print(f'File "{filepath}" already exists')
            return 1
        with open(filepath, "wb+") as file:
            file.write(b"<numPages></numPages>\n<page1>\n<numRecords></numRecords>\n</page1>")
        return 0


    def create_table_cmd(self, query:list): #TODO
        startIdx = 3
        attributes = {} # Initialize dictionary to hold attributes (name, type) NOTE if key=primarykey value=column name
        tblName = query[2]

        # Steup
        if "()" in tblName:
            print("Table with no attributes")
            return 1
        elif "(" in tblName:
            tblName = tblName[:-1]
        elif query[startIdx] == "(":
            startIdx = 4

        # if self.Catalog.table_exists(tblName) == 1:
        #     print("Table of name foo already exists")
        #     return 1
        
        # Loop through attributes
        i = startIdx
        while i < len(query):
            if query[i] == ")":
                break

            name = query[i]
            dType = query[i+1]
            
            if "))" in dType:
                dType = dType[:-1]

            if name in attributes.keys():
                print(f'Duplicate attribute name "{name}"')
                return 1

            if self.checkDtype(dType) == 1:
                print(f'Invalid data type "{dType}"')
                return 1

            if "," in dType:
                dType = dType.rstrip(',')
                attributes[name] = dType
                i += 2
                continue
            elif len(query) <= i+2:
                attributes[name] = dType
                break
            
            if "primarykey" in query[i+2] and "primarykey" not in attributes.keys():
                query[i+2].rstrip(',')
                attributes[name] = dType
                attributes["primarykey"] = name
                i += 3
            elif "primarykey" in query[i+2] and "primarykey" in attributes.keys():
                print("More than 1 primary key")
                return 1
            else:
                attributes[name] = dType
                i += 2
        
        if "primarykey" not in attributes.keys():
            print("No primary key defined")
            return 1


        print("Attributes:", attributes) # NOTE Temporary

        # TODO Update Catalog
        # Catalog.add_table(tblName, attributes)


        if self.buildTableFile(tblName, attributes) == 1:
            return 1
        
        return 0


    def select_cmd(self, query): #TODO
        attributes = []
        for i in range(len(query)):
            if query[i] == "from":
                tableName = query[i+1]

        # TODO check if table exists
            # if doesn't exist: print("No such table foo")
            # return 1 # implying error
        # else loop through table printing the selected attribute
            # if attribute = "*" print all
        
        if query[1] == "*": # TODO Will need to update for later phases
            attributes.append(query[1])
        
        return 0


    def insert_cmd(self, query:list): #TODO
        """ERROR Examples
        [] No such table foo
        [] row (3.2): Invalid data type: expected (integer) got (dobule).
        [] row (1 3.2): Too many attributes: expected (integer) got (integer double)
        [] Duplicate primary key for row (1)
        [] row (3.2 "helloworld"): char(5) can only accept 5 chars; "helloworld" is 10
        [] row ("hello", 3.2): Invalid data types: expected (double char(5)) got (char(5) double)
        """
        attributes = []
        tblName = query[2]
        query = query[4:]

        queryStr = ' '.join(query)

        loop = True
        while loop: # Each loop builds a tuple of row values and adds tuple to attributes list
            vals = [] # list to hold each element in a row
            curVal = "" # Current value being built
            for i in range(len(queryStr)):
                if queryStr[i] == "(" or queryStr[i] == ',':
                    pass
                elif queryStr[i] == ")":
                    if i == len(queryStr) - 1:
                        vals.append(curVal)
                        loop = False
                        queryStr = queryStr[i+1:]
                        break
                    else:
                        vals.append(curVal)
                        queryStr = queryStr[i+1:]
                        break
                elif queryStr[i] == ' ':
                    vals.append(curVal)
                    curVal = ""
                else:
                    curVal += queryStr[i]
                    
            attributes.append(tuple(vals))
        
        print("Table Name:", tblName)
        print("Attributes:", attributes)
        print("\n")
        return 1


    def display_schema_cmd(self): #TODO
        print(f"DB location: {self.dbloc}\nPage Size: {self.pageSize}\nBuffer Size: {self.bufferSize}\n")
        # Get schema info from catalog
        # if no tables print("No tables to display")
        # else loop through tables printing
        # if fail return 1 implying ERROR
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
                status = self.display_schema_cmd()
                return  status
            elif query[1] == "info":
                try:
                    status = self.display_info_cmd(query[2])
                    return  status
                except IndexError:
                    return 1
            else:
                return 1 # Return Failure
        elif query[0] == "select":
            status = self.select_cmd(query)
            return status
        elif query[0] == "insert" and query[1] == "into" and query[3] == "values":
            status = self.insert_cmd(query)
            return status
        elif query[0] == "create" and query[1] == "table":
            status = self.create_table_cmd(query)
            return  status
        
        status = 1 #Bad status
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
    print(f"Exit Code: {QP.main()}")
