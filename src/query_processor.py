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


def create_table_cmd(): #TODO
    return


def select_cmd(attribute, tableName): #TODO
    # if table doesnt exist
    print("No such table foo")
    return 1 # implying error
    # else loop through table printing the selected attribute
        # if attribute = "*" print all
    # return 0  implying success


def insert_cmd(): #TODO
    return


def display_schema_cmd(query:list, dbloc, pageSize, bufferSize): #TODO
    print(f"DB location: {dbloc}\nPage Size: {pageSize}\nBuffer Size: {bufferSize}\n")
    # TODO:
    # if no tables
    print("No tables to display")
    # else loop through tables printing
    #   if fail return 1 implying ERROR
    return 0 # implying SUCCESS


def display_info_cmd(tableName): #TODO
    # TODO:
    tableSchema = "schema"
    tablePages = 0
    tableRecords = 0
    # if table exists
    print(f"Table name: {tableName}\nTable schema:\n\t{tableSchema}\nPages: {tablePages}\nRecords: {tableRecords}")
    # else return 1 implying ERROR
    return 0 #implying SUCCESS


def help(): #TODO
    """
    Print the help message to the user.
    """
    print("HELP:\n\t- CREATE: //insert create usage here\n\tSELECT: //insert select usage here\n\t-INSERT: //insert insert usage here\n\tDISPLAY [\n\t\tSCHEMA: //insert display schema usage here\n\t\tINFO - //insert display info usage here\n\t\t]")
    return 0


def process_input(query:list, dbloc, pageSize, bufferSize):
    """
    Process query after checking if valid input. Depending on the command entered,
    call the necessary function to execute the query and then return.
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
        print("TODO") #TODO
        return 1 # TEMPORARY RETURN
    elif query[0] == "create" and query[1] == "table":
        print("TODO") #TODO
        return 1 # TEMPORARY RETURN
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
        print(inputs) #TEMPORARY
        status = process_input(inputs, dbloc, pageSize, bufferSize) # Call process input and return status code
        if status == 0:
            print("SUCCESS\n") # Successfully completed query
        else:
            print("ERROR\n") # Error completing query
    return 0


if __name__ == '__main__':
    main()
    pass
