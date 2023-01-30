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
    """
    This commmand will be used to create the schema for a table. This schema will
    be added to the catalog. This schema will be used by the system to
    store/access/update/delete data in the created table.

    :param <>: description

    :return: description
    """
    return


def select_cmd():
    """

    :param <>: description

    :return:
    """
    return


def insert_cmd():
    """

    :param <>: description

    :return:
    """
    return


def display_schema_cmd():
    """

    :param <>: description

    :return:
    """
    return


def display_info_cmd():
    """

    :param <>: description

    :return:
    """
    return

"""
print a helpful message
"""
def help():
    return "HELP:\n\t- CREATE: //insert create usage here\n\tSELECT: //insert select usage here\n\t-INSERT: //insert insert usage here\n\tDISPLAY [\n\t\tSCHEMA: //insert display schema usage here\n\t\tINFO - //insert display info usage here\n\t\t]"


"""
Kick start main text processing loop (while loop) that awaits for a ; to end a statement or an exit command.\
NOTE: Carriage returns are ignored.
"""
def main():
    go = True
    # readInput = input("> ")
    while go:        
        readInput = input("> ")
        if readInput == "exit":
            go = False
            continue

        if readInput.lower() == "help":
            print(help())
            continue

        while not ";" in readInput:
            readInput += " " + input()
        print(readInput)

        


if __name__ == '__main__':
    main()
    pass
