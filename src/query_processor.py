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


def create_table_cmd():
    return


def select_cmd(attribute, tableName):
    # if table doesnt exist
    print("No such table foo")
    return 1 # implying error
    # else loop through table printing the selected attribute
        # if attribute = "*" print all
    # return 0  implying success

def insert_cmd():
    return

def display_schema_cmd():
    # TODO:
    # if no tables
    print("No tables to display")
    # else loop through tables printing
    #   if fail return 1 implying ERROR
    return 0 # implying SUCCESS


def display_info_cmd(tableName):
    # TODO:
    tableSchema = "schema"
    tablePages = 0
    tableRecords = 0
    # if table exists
    print(f"Table name: {tableName}\nTable schema:\n\t{tableSchema}\nPages: {tablePages}\nRecords: {tableRecords}")
    # else return 1 implying ERROR
    return 0 #implying SUCCESS

"""
print a helpful message
"""
def help():
    return "HELP:\n\t- CREATE: //insert create usage here\n\tSELECT: //insert select usage here\n\t-INSERT: //insert insert usage here\n\tDISPLAY [\n\t\tSCHEMA: //insert display schema usage here\n\t\tINFO - //insert display info usage here\n\t\t]"


"""
Kick start main text processing loop (while loop) that awaits for a ; to end a statement or an exit command.\
NOTE: Carriage returns are ignored.
NOTE: Still keeps things that come after the ; in the input (as long as it is on the same line) this can be changed.
"""
def main(dbloc, pageSize, bufferSize):
    print("\nPlease enter commands, enter <quit> to shutdown the db\n")
    go = True
    returnCode = 0 # Good return
    while go:
        status = 0
        readInput = input("JottQL> ")
        if readInput == "<quit>":
            go = False
            continue
        while not ";" in readInput:
            readInput += input()
        readInput = readInput.lower()
        inputs = readInput.split(';')[0].split(" ")
        if inputs[-1] == "":
            inputs.remove(inputs[-1])
        print(inputs)
        if inputs[0] == "help":
            print(help())
        elif inputs[0] == "display":
            if inputs[1] == "schema":
                print(f"DB location: {dbloc}\nPage Size: {pageSize}\nBuffer Size: {bufferSize}\n")
                status = display_schema_cmd()
            elif inputs[1] == "info":
                status = display_info_cmd(inputs[2])
            else:
                status = 1
        elif inputs[0] == "select" and inputs[2] == "from":
            status = select_cmd(inputs[1], inputs[3])
        elif inputs[0] == "insert": print("")
            # TODO:
        elif inputs[0].lower() == "create": print("")
            # TODO:
        else:
            status = 1 # bad input
        if status == 0:
            print("SUCCESS\n")
        else:
            print("ERROR\n")
    return returnCode


if __name__ == '__main__':
    main()
    pass
