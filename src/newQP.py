import re
BAD_STATUS = 1
GOOD_STATUS = 0

def process_select(strManipulate):
    selectCommands = {
        "name": "",
        "select": [],
        "where": [],
        "orderby": ""
    }
    if "from" not in strManipulate:
            print(f"No FROM in command")
            return BAD_STATUS

    selectArgs = strManipulate[:strManipulate.index("from")]
    selectCommands["select"] = selectArgs.replace(" ", "").split(",") #Remove whitespace from selectArgs and split on commas

    if len(strManipulate) < strManipulate.index("from " + len("from ")):
            print("Bad formatting")
            return BAD_STATUS
    
    strManipulate = strManipulate[strManipulate.index("from ") + len("from "):]
    if "where" not in strManipulate and "orderby" not in strManipulate:
        selectCommands["name"] = strManipulate.replace(" ", "") # Should just be the table name left, but make sure no trailing spaces
    
    elif "where" in strManipulate and "orderby" not in strManipulate:
        selectCommands["name"] = strManipulate[:strManipulate.index("where")].replace(" ", "")
        strManipulate = strManipulate[strManipulate.index("where ") + len("where "):]
        selectCommands["where"] = strManipulate.strip()
    elif "where" not in strManipulate and "orderby" in strManipulate:
        selectCommands["name"] = strManipulate[:strManipulate.index("orderby")].replace(" ", "")
        strManipulate = strManipulate[strManipulate.index("orderby ") + len("orderby "):]
        selectCommands["orderby"] = strManipulate.strip()
    elif "where" in strManipulate and "orderby" in strManipulate:
        selectCommands["name"] = strManipulate[:strManipulate.index("where")].replace(" ", "")
        strManipulate = strManipulate[strManipulate.index("where ") + len("where "):]
        selectCommands["where"] = strManipulate[:strManipulate.index("orderby")]
        strManipulate = strManipulate[strManipulate.index("orderby ") + len("orderby "):]
        selectCommands["orderby"] = strManipulate.strip()

    
    # TODO: test for table name
    # TODO: test for column names

    return selectCommands

def process_insert(strManipulate):
    insertCommands = {
            "name": "",
            "values": []
        }
    if strManipulate[:strManipulate.index(" ")] != "into":
        print("Second argument must be into")
    strManipulate = strManipulate[strManipulate.index("into ") + len("into "):] # drop "into"
    if "values" not in strManipulate:
        print("No values keyword found")
        return BAD_STATUS
    insertCommands["name"] = strManipulate[:strManipulate.index("values")]
    strManipulate = strManipulate[strManipulate.index("values ") + len("values "):]

    attributes = process_attributes(strManipulate)

    for i in attributes:
        insertCommands["values"].append(i)

    #TODO check table valid
    #TODO check values in attributes match catalog and evaluate

    return insertCommands

def process_attributes(strManipulate):
    #All thats left is (hopefully) the tuples for inserting statments.
    insertValues = strManipulate.split(",")
    attributes = []
    for value in insertValues:
        if "(" in value:
            value = value.replace("(","")
        if ")" in value:
            value = value.replace(")","")
        processedInsertVal = value.split(" ")
        for i in range(len(value)):
            if i+2 > len(processedInsertVal):
                break
            if processedInsertVal[i].count('"') == 1:
                tempVal = [' '.join([processedInsertVal[i], processedInsertVal[i+1]])]
                processedInsertVal[i+1] = ""
                processedInsertVal[i] = ""
                processedInsertVal = insert_into_array(processedInsertVal, i, tempVal)
                processedInsertVal = remove_blank_entries(processedInsertVal)
        attributes.append(processedInsertVal)
    return attributes

def process_create(strManipulate):
    create_commands = {
        "name" : "",
        "pageCount" : 0,
        "recordCount" : 0,
        "attributes" : []
    }
    isNextCommandTable = strManipulate[:strManipulate.index(" ")] == "table"
    if not isNextCommandTable:
        print("Error: Create <table>")
        return BAD_STATUS
    if "()" in strManipulate:
        print("Empty Attributes")
        return BAD_STATUS
    
    strManipulate = strManipulate[strManipulate.index("table") + len("table "):]
    tableName = strManipulate[:strManipulate.index("(")].replace(" ","") #foo ( or foo(
    create_commands["name"] = tableName

    strManipulate = strManipulate[strManipulate.index('(') + len("("):]
    attributes = process_attributes(strManipulate) # Never gonna be more than one tuple.

    pkCount = 0
    attributes_found = []
    for attribute in attributes:
        # attribute = attribute.split(" ")
        attribute = remove_blank_entries(attribute)
        temp_Attrib = {
            "name" : attribute[0],
            "type" : attribute[1],
            "primary_key" : "primarykey" in attribute, #Technically could be in position 3, 4, or 5
            "unique" : "unique" in attribute,
            "notnull" : "notnull" in attribute
        }
        create_commands["attributes"].append(temp_Attrib)
        if attribute[0] not in attributes_found:
            attributes_found.append(attribute[0])
        else:
            print("Duplicate keys")
            return BAD_STATUS
        if "primarykey" in attribute:
            pkCount += 1

    if pkCount == 0:
        print("No Primarykey found")
        return BAD_STATUS
    if pkCount > 1:
        print("Too many primary keys")
        return BAD_STATUS
    
    return create_commands

def processInput(readInput):
    try:
        readInput = readInput[:-1] #Remove ;
        command = readInput.split(" ")[0] # Get the command
        strManipulate = readInput[readInput.index(command) + len(command+" ")]
        if " " not in readInput:
            print("Incorrect formatting for statement")
            return BAD_STATUS
        strManipulate = readInput[readInput.index(" ")+1:] # start from after the next space
        if command == "select":
            return process_select(strManipulate)
        elif command == "insert":
            return process_insert(strManipulate)
        elif command == "create":
            create_commands = process_create(strManipulate)
            return create_commands
        elif command == "display":
            pass
        elif command == "drop":
            pass
        elif command == "alter":
            pass
        elif command == "delete":
            pass
        elif command == "update":
            pass
        else:
            print(f"Bad command passed {command}")
            return BAD_STATUS
        return GOOD_STATUS
    except ValueError:
        print(f"Error with formatting {readInput}")
        return BAD_STATUS
    except Exception as e:
        print("Undiagnosed error caught.")
        print(e)
        return BAD_STATUS
    
def insert_into_array(arr, index, arr_to_insert):
    """
    Insert a given array  of characters (typically the same characters but split on a different delimeter) into an index
    Example:
        ['select', 'one', 'two', 'three', 'from', 'foo', 'where', 'x', '=', '1', 'and', ** 'orderby', 'x;']
        (In this example the given index was the y=2, but the program assumes that it has been removed)
        --> 
        ['select', 'one', 'two', 'three', 'from', 'foo', 'where', 'x', '=', '1', 'and', *'y', '=', '2'*, 'orderby', 'x;']

    NOTE: This can easily be updated to simply insert without removing the element from the list by removing the index+1 on the right var

    Args:
        arr (array): original array containing element to replace
        index (int): index of element to be replaced
        arr_to_insert (array): the array to be inserted

    Returns:
        array : updated array after replacement.
    """
    left = arr[:index]
    right = arr[index:]
    return [*left, *arr_to_insert, *right]

def remove_blank_entries(passedArray):
        """
        Remove blank strings from array entry

        Args:
            passedArray (arr): input list of commands

        Returns:
            array: cleaned input list
        """
        return [element for element in passedArray if element != "" if element != " "]

def main():
    while True:
        try:
            readInput = input("> ").lower()
            if not ";" in readInput:
                readInput += input()
            
            print(f"input string:\t{readInput}")
            processed_args = processInput(readInput)
            if processed_args == BAD_STATUS:
                print("ERROR")
                continue
            print(f"Processed Commands:\t{processed_args}")
        except KeyboardInterrupt:
            print("\nExited")
            exit()

if __name__ == '__main__':
    main()



