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

class QueryProcessor:

    def __init__(self, dbloc, pageSize, bufferSize) -> None:
        self.dbloc = dbloc
        self.pageSize = pageSize
        self.bufferSize = bufferSize
        self.Catalog = catalog.Catalog(dbloc, pageSize, bufferSize)


    def check_data_type(self, d_type):
        """
        Helper function for create_table_cmd().
        Checks if an attributes data type is valid.
        """
        if "," in d_type: d_type = d_type.rstrip(',')
        valid_types = ['integer', 'double', 'boolean'] # 'char(n)', 'varchar(n)'
        if "varchar" in d_type:
            n = re.findall("^varchar\(\d+\)$", d_type)
            if len(n) == 1: 
                return 0
            else: 
                return 1
        elif "char" in d_type:
            n = re.findall("^char\(\d+\)$", d_type)
            if len(n) == 1: return 0
            else: return 1
        elif d_type in valid_types:
            return 0
        else:
            return 1


    def create_table_cmd(self, query:list):
        """
        Creates the schema for a table. The schema is added to the catalog.
        The schema will be used by the system to store/access/update/delete
        data in the table.
        """
        start_idx = 3
        attributes = {} # Initialize dictionary to hold attributes (name, type) NOTE if key=primarykey value=column name
        table_name = query[2]

        # Steup
        if "()" in table_name:
            print("Table with no attributes")
            return 1
        elif "(" in table_name:
            table_name = table_name[:-1]
        elif query[start_idx] == "(":
            start_idx = 4

        # Check catalog
        if self.Catalog.table_exists(table_name) == 1:
            print("Table of name foo already exists")
            return 1
        
        # Loop through attributes
        i = start_idx
        while i < len(query):
            if query[i] == ")":
                break

            name = query[i]
            d_type = query[i+1]
            
            if "))" in d_type:
                d_type = d_type[:-1]

            if name in attributes.keys():
                print(f'Duplicate attribute name "{name}"')
                return 1

            if self.check_data_type(d_type) == 1:
                print(f'Invalid data type "{d_type}"')
                return 1

            if "," in d_type:
                d_type = d_type.rstrip(',')
                attributes[name] = d_type
                i += 2
                continue
            elif len(query) <= i+2:
                attributes[name] = d_type
                break
            
            if "primarykey" in query[i+2] and "primarykey" not in attributes.keys():
                query[i+2].rstrip(',')
                attributes[name] = d_type
                attributes["primarykey"] = name
                i += 3
            elif "primarykey" in query[i+2] and "primarykey" in attributes.keys():
                print("More than 1 primary key")
                return 1
            else:
                attributes[name] = d_type
                i += 2
        
        if "primarykey" not in attributes.keys():
            print("No primary key defined")
            return 1

        print("Attributes:", attributes) # NOTE Temporary

        # Add the table to catalog
        self.Catalog.add_table(table_name, attributes)
        
        return 0 # Update return based off storage manager


    def select_cmd(self, query): #TODO
        """
        Access data in tables. Will display all of the data in the table in
        an easy to read format, including column names.
        """
        attributes = []
        for i in range(len(query)):
            if query[i] == "from":
                table_name = query[i+1]
        
        if query[1] == "*": # NOTE Will need to update for later phases
            attributes.append(query[1])
        
        print("Table Name:", table_name) # NOTE Temporary
        print("Attributes:", attributes) # NOTE Temporary
        print("\n") # NOTE Temporary
        
        return 0 # NOTE update return based off storage manager


    def insert_cmd(self, query:list): #TODO
        """
        Insert tuple(s) of information into a table.
        """
        attributes = []
        table_name = query[2]
        query = query[4:]

        query_str = ' '.join(query)

        loop = True
        while loop: # Each loop builds a tuple of row values and adds tuple to attributes list
            vals = [] # list to hold each element in a row
            cur_val = "" # Current value being built
            for i in range(len(query_str)):
                if query_str[i] == "(" or query_str[i] == ',':
                    pass
                elif query_str[i] == ")":
                    if i == len(query_str) - 1:
                        vals.append(cur_val)
                        loop = False
                        query_str = query_str[i+1:]
                        break
                    else:
                        vals.append(cur_val)
                        query_str = query_str[i+1:]
                        break
                elif query_str[i] == ' ':
                    vals.append(cur_val)
                    cur_val = ""
                else:
                    cur_val += query_str[i]
                    
            attributes.append(tuple(vals))
        
        print("Table Name:", table_name) # NOTE TEMPORARY
        print("Attributes:", attributes) # NOTE TEMPORARY
        print("\n") # NOTE TEMPORARY
        return 1 # update return based off storage manager


    def display_schema_cmd(self): #TODO
        """
        Displays the catalog of the database in an easy to read format.
        Including: Database location, page size, buffer size, table schema.
        """
        print(f"DB location: {self.dbloc}\nPage Size: {self.pageSize}\nBuffer Size: {self.bufferSize}\n")
        # Get schema info from catalog
        # if no tables print("No tables to display")
        # else loop through tables printing
        # if fail return 1 implying ERROR
        return 0 # SUCCESS


    def display_info_cmd(self, table_name): #TODO
        """
        Calls print_table from Catalog to print given Table Names information.
        Including: Table name, table schema, number of pages, number of records.
        All output comes from Catalog.print_table.
        """
        if self.Catalog.print_table(table_name) == 1:
            return 1 # FAILURE

        return 0 # SUCCESS


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
                return 1
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

        Good status = 0 (Prints SUCCESS)
        Bad status = !0 (Prints ERROR)
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
