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


def create_table_cmd(query:list): #TODO
    
    return 1


def select_cmd(attribute, tableName): #TODO
    # if table doesnt exist
    print("No such table foo")
    return 1 # implying error
    # else loop through table printing the selected attribute
        # if attribute = "*" print all
    # return 0  implying success


def insert_cmd(query:list): #TODO
    return 1


def display_schema_cmd(query:list, dbloc, pageSize, bufferSize): #TODO
    print(f"DB location: {dbloc}\nPage Size: {pageSize}\nBuffer Size: {bufferSize}\n")
    # if no tables
    print("No tables to display")
    # else loop through tables printing
    #   if fail return 1 implying ERROR
    return 0 # implying SUCCESS


def display_info_cmd(tableName): #TODO
    tableSchema = "schema"
    tablePages = 0
    tableRecords = 0
    # if table exists
    print(f"Table name: {tableName}\nTable schema:\n\t{tableSchema}\nPages: {tablePages}\nRecords: {tableRecords}")
    # else return 1 implying ERROR
    return 0 #implying SUCCESS


def help():
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


def process_input(query:list, dbloc, pageSize, bufferSize):
    """
    Process query. Depending on the command entered, call the 
    necessary function to execute the query and then return.
    Returns 0 if success and 1 if failure.
    """
    if query[0] == "help":
        return help() # Return status code
    elif query[0] == "display":
        if query[1] == "schema":
            return display_schema_cmd(query, dbloc, pageSize, bufferSize) # Return status code
        elif query[1] == "info":
            return display_info_cmd(query[2]) # Return status code
        else:
            return 1 # Return Failure
    elif query[0] == "select" and query[2] == "from":
        return select_cmd(query[1], query[3]) # Return status code
    elif query[0] == "insert" and query[1] == "into":
        return insert_cmd(query) # Return status code
    elif query[0] == "create" and query[1] == "table":
        return create_table_cmd(query) # Return status code
    return 1 # Return failure if command is not valid


def main(dbloc, pageSize, bufferSize):
    """
    Kick start main text processing loop (while loop) that awaits for a ; to end a statement or an exit command.
    NOTE: Carriage returns are ignored.
    NOTE: Still keeps things that come after the ; in the input (as long as it is on the same line) this can be changed.
    """
    print("\nPlease enter commands, enter <quit> to shutdown the db\n")
    go = True
    while go:
        status = 0 # Holds status of input / if success or error
        readInput = input("JottQL> ")
        if readInput == "<quit>": # Handle quit command from user
            go = False # Set go to False
            continue # Return to start of loop (will exit loop since go is set to False)
        while not ";" in readInput: # Continue accepting input until ";" is entered
            readInput += " " + input() # Append to readInput
        readInput.lower() # Make input lowercase
        inputs = readInput.split(';')[0].split(" ") # Split input string and store in a list
        inputs = [x for x in inputs if x != ''] # Cleanup inputs list by removing all blank values
        print("INPUT LIST:", inputs) #TEMPORARY
        status = process_input(inputs, dbloc, pageSize, bufferSize) # Call process input and return status code
        if status == 0:
            print("SUCCESS\n") # Successfully completed query
        else:
            print("ERROR\n") # Error completing query
    return 0


if __name__ == '__main__':
    main()
    pass
