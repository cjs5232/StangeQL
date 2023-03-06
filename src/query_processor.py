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
import storage_manager

BAD_STATUS = 1
GOOD_STATUS = 0

class QueryProcessor:

    def __init__(self, dbloc, pageSize, bufferSize) -> None:
        self.dbloc = dbloc
        self.pageSize = pageSize
        self.bufferSize = bufferSize
        self.cat = catalog.Catalog(dbloc, pageSize, bufferSize)
        self.StorageM = storage_manager.StorageManager(dbloc, pageSize, bufferSize)

        self.inputString = ""
        self.command_args = []
        self.command_prefix = []

        self.keywords = ["select", "create", "insert", "delete", "update", "display", "where", "set", "from", "orderby", "and", "or", "table", "notnull", "unique", "primarykey", "alter", "drop", "add", "default"]

    def main(self):
        """
        Kick start main text processing loop (while loop) that awaits for a ; to end a statement or an exit command.
        NOTE: Carriage returns are ignored.

        Good status = 0 (Prints SUCCESS)
        Bad status = !0 (Prints ERROR)
        """
        print("\nPlease enter commands, enter <quit> to shutdown the db\n")

        while True:
            status = 0 
            readInput = input("JottQL> ").lower()
            if readInput == "<quit>":
                return status
            if readInput == "<help>":
                self.help()
                continue
            while not ";" in readInput:
                readInput += " " + input().lower()

            processed_args = self.processInput(readInput)
            if processed_args == BAD_STATUS:
                print("ERROR")
                continue

            if status == 0:
                print("SUCCESS\n")
            else:
                print("ERROR\n")

    def processInput(self, readInput):
        try:
            readInput = readInput[:-1] #Remove ;
            command = readInput.split(" ")[0] # Get the command
            str_manipulate = readInput[readInput.index(command) + len(command+" ")]
            if " " not in readInput:
                print("Incorrect formatting for statement")
                return BAD_STATUS
            str_manipulate = readInput[readInput.index(" ")+1:] # start from after the next space
            if command == "select":
                return self.process_select(str_manipulate)
            elif command == "insert":
                return self.process_insert(str_manipulate)
            elif command == "create":
                return self.process_create(str_manipulate)
            elif command == "display":
                return self.process_display(str_manipulate)
            elif command == "drop":
                return self.process_drop(str_manipulate)
            elif command == "alter":
                is_next_table = str_manipulate[:str_manipulate.index(" ")] == "table"
                if not is_next_table:
                    print("Error: Alter <table>")
                    return BAD_STATUS
                str_manipulate = str_manipulate[str_manipulate.index("table") + len("table "):]
                table_name = str_manipulate[:str_manipulate.index(" ")]
                if self.does_table_exist(table_name) == 1:
                    return BAD_STATUS
                str_manipulate = str_manipulate[str_manipulate.index(table_name) + len(table_name) + 1:]
                # drop attrib_name
                # add a_name a_type default value
            elif command == "delete":
                pass
            elif command == "update":
                pass
            else:
                print(f"Bad command passed {command}")
                return BAD_STATUS
        except ValueError:
            print(f"Error with formatting {readInput}")
            return BAD_STATUS
        except Exception as e:
            print("Undiagnosed error caught.")
            print(e)
            return BAD_STATUS

    def process_create(self, str_manipulate):
        create_commands = {
            "name" : "",
            "pageCount" : 0,
            "recordCount" : 0,
            "attributes" : []
        }
        is_next_table = str_manipulate[:str_manipulate.index(" ")] == "table"
        if not is_next_table:
            print("Error: Create <table>")
            return BAD_STATUS
        if "()" in str_manipulate:
            print("Empty Attributes")
            return BAD_STATUS
        
        str_manipulate = str_manipulate[str_manipulate.index("table") + len("table "):]
        table_name = str_manipulate[:str_manipulate.index("(")].replace(" ","") #foo ( or foo(
        create_commands["name"] = table_name

        does_table_exist = self.cat.table_exists(table_name)
        if does_table_exist == 1:
            print(f"Table of name {table_name} already exists")
            return BAD_STATUS

        str_manipulate = str_manipulate[str_manipulate.index('(') + len("("):]
        attributes = self.process_attributes(str_manipulate) # Never gonna be more than one tuple.

        primary_key_count = 0
        attributes_found = []
        for attribute in attributes:
            # attribute = attribute.split(" ")
            attribute = self.remove_blank_entries(attribute)
            temp_Attrib = {
                "name" : attribute[0],
                "type" : attribute[1],
                "primarykey" : "primarykey" in attribute, #Technically could be in position 3, 4, or 5
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
                primary_key_count += 1

        if primary_key_count == 0:
            print("No Primarykey found")
            return BAD_STATUS
        if primary_key_count > 1:
            print("Too many primary keys")
            return BAD_STATUS
        
        status = self.cat.add_table(create_commands)
        return status
    
    def process_insert(self, str_manipulate):
        insert_commands = {
                "name": "",
                "values": []
            }
        if str_manipulate[:str_manipulate.index(" ")] != "into":
            print("Second argument must be into")
        str_manipulate = str_manipulate[str_manipulate.index("into ") + len("into "):] # drop "into"
        if "values" not in str_manipulate:
            print("No values keyword found")
            return BAD_STATUS
        table_name = str_manipulate[:str_manipulate.index("values")]
        str_manipulate = str_manipulate[str_manipulate.index("values ") + len("values "):]

        insert_commands["name"] = table_name

        attributes = self.process_attributes(str_manipulate)
        for i in attributes:
            insert_commands["values"].append(i)

        does_table_exist = self.cat.table_exists(table_name)
        if does_table_exist == 1:
            print(f"Table of name {table_name} already exists")
            return BAD_STATUS
        #TODO check values in attributes match catalog and evaluate

        # attributes = self.cat.table_attributes(table_name)
        # if attributes == 1:
            # return BAD_STATUS

        #result = self.StorageM.insert_record(table_name, attributes, values)
        #return result # update return based off storage manager

        return GOOD_STATUS
    
    def process_select(self, str_manipulate):
        select_commands = {
            "name": "",
            "select": [],
            "where": [],
            "orderby": ""
        }
        if "from" not in str_manipulate:
                print(f"No FROM in command")
                return BAD_STATUS

        select_args = str_manipulate[:str_manipulate.index("from")]
        select_commands["select"] = select_args.replace(" ", "").split(",") #Remove whitespace from select_args and split on commas

        if len(str_manipulate) < str_manipulate.index("from " + len("from ")):
                print("Bad formatting")
                return BAD_STATUS
        
        str_manipulate = str_manipulate[str_manipulate.index("from ") + len("from "):]
        where_and_orderby = self.process_where_orderby(str_manipulate)
        if where_and_orderby == 1:
            return BAD_STATUS
        
        name, where, orderby = where_and_orderby
        
        select_commands["name"] = name
        select_commands["where"] = where
        select_commands["orderby"] = orderby
        
        table_exists = self.does_table_exist(name)
        if table_exists != 0:
            return BAD_STATUS
        
        data = self.StorageM.get_records(name)
        if data == 1:
            return BAD_STATUS
        
        # TODO: test for column names <-- Do i have to or will this error be handled in the SM?

        # Get column names from catalog
        columns = []
        attributes = self.cat.table_attributes(name)

        if attributes == 1:
            return BAD_STATUS
        
        for i in attributes:
            columns.append(i['name'])

        # Find necessary padding for columns and store in column_width
        length_list = [len(str(element)) for row in data for element in row]
        for i in columns:
            length_list.append(len(i))
        column_width = max(length_list)

        # Format columns and barriers
        columns_formatted = "|".join(str(element).center(column_width +2) for element in columns)
        columns_formatted = "|" + columns_formatted + "|"
        horizontal_lines = "-" * (len(columns_formatted))

        # Print column section
        print(horizontal_lines)
        print(columns_formatted)
        print(horizontal_lines)

        # Print rows
        for row in data:
            row = "|".join(str(element).center(column_width + 2) for element in row)
            row = "|" + row + "|"
            print(row)
        print("\n")
        return GOOD_STATUS
    
    def process_display(self, str_manipulate):
        """
        Usage display [info/schema];

        Display schema
            This command will display the catalog of the database in an easy to read format. For this
            phase it will just display:
            • database location
            • page size
            • buffer size
            • table schema

        Display Info
            This command will display the information about a table in an easy to read format. Tt will
            display:
            • table name
            • table schema
            • number of pages
            • number of records
            The command will be display info <name>;
        

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """
        
        command_args = str_manipulate.split(" ")

        if len(command_args) < 2:
            print(f"Incorrect format: More values expected for {command_args}")
            return BAD_STATUS
        if command_args[1] == "schema":
            return self.display_schema()
        elif command_args[1] == "info":
            if self.cat.print_table(command_args[2]) == 1:
                return BAD_STATUS # FAILURE
        else:
            print("Incorrect format")
            return BAD_STATUS
    
    def display_schema(self) -> int:
        """
        Displays the catalog of the database in an easy to read format.
        Including: Database location, page size, buffer size, table schema.
        """
        tables = []
        print(f"DB location: {self.dbloc}\nPage Size: {self.pageSize}\nBuffer Size: {self.bufferSize}\n")
        
        catalog = self.cat.get_catalog()

        if catalog == 1:
            return BAD_STATUS
        
        for i in catalog['tables']:
            tables.append(i['name'])
        
        if len(tables) == 0:
            print("\nNo tables to display")
            return GOOD_STATUS
        
        print("\nTables:\n")
        
        for i in range(len(tables)):
            self.cat.print_table(tables[i])
            if i < len(tables) - 1:
                print("\n")
        
        return GOOD_STATUS

    def process_drop(self, str_manipulate):
        is_next_table = str_manipulate[:str_manipulate.index(" ")] == "table"
        if not is_next_table:
            print("Error: drop <table>")
            return BAD_STATUS
        table_name = str_manipulate[str_manipulate.index("table") + len("table "):]
        if self.does_table_exist(table_name) != 0:
            return BAD_STATUS
        # TODO call drop on table
        return GOOD_STATUS

    def check_data_type(self, d_type:str) -> int:
        """
        Helper function for create_table_cmd().
        Checks if an attributes data type is valid or not and
        returns the status code.
        """
        if "," in d_type: d_type = d_type.rstrip(',')
        valid_types = ['integer', 'double', 'boolean'] # 'char(n)', 'varchar(n)'
        if "varchar" in d_type:
            n = re.findall("^varchar\(\d+\)$", d_type)
            if len(n) == 1: 
                return GOOD_STATUS
            else: 
                return BAD_STATUS
        elif "char" in d_type:
            n = re.findall("^char\(\d+\)$", d_type)
            if len(n) == 1: return GOOD_STATUS
            else: return BAD_STATUS
        elif d_type in valid_types:
            return GOOD_STATUS
        else:
            return BAD_STATUS

    def select_cmd_deprecated(self, query:list) -> int:
    #     """
    #     Parse select query and use storage manager to access data.
    #     Once data is returned from storage manager, get the table column
    #     names from the catalog and output the table in a clean/formatted
    #     way.

    #     Access data in tables. Will display all of the data in the table in
    #     an easy to read format, including column names.
    #     """
    #     attributes = []

    #     if "from" not in query:
    #         print('"from" keyword missing in select query')
    #         return BAD_STATUS

    #     for i in range(len(query)):
    #         if query[i] == "from":
    #             table_name = query[i+1]
        
    #     # Check catalog
    #     does_table_exist = self.cat.table_exists(table_name)
    #     if does_table_exist == 0: # 0 meaning table does NOT exist
    #         print(f"No such table {table_name}")
    #         return BAD_STATUS
    #     elif does_table_exist == 2: # 2 meaning no catalog found
    #         return BAD_STATUS
        
    #     if query[1] == "*":
    #         attributes.append(query[1])
    #     else: # Assume single primary key select 
    #         attributes.append(query[1]) # TODO: fix this to check for non-primary key?
    #         # print(f"Invalid selection: {query[1]}")
    #         # return BAD_STATUS
        
    #     # Get Data from Storage Manager: Expecting return: data = [(), (), ...]
    #     data = self.StorageM.get_records(table_name)
    #     if data == 1:
    #         return BAD_STATUS

    #     # Get column names from catalog
    #     columns = []
    #     attributes = self.cat.table_attributes(table_name)

    #     if attributes == 1:
    #         return BAD_STATUS
    #     else:
    #         for i in attributes:
    #             columns.append(i['name'])
        return GOOD_STATUS
    
    def print_select_query_deprecated(arrayPassed):
        #     # Find necessary padding for columns and store in column_width
        #     length_list = [len(str(element)) for row in data for element in row]
        #     for i in columns:
        #         length_list.append(len(i))
        #     column_width = max(length_list)

        #     # Format columns and barriers
        #     columns_formatted = "|".join(str(element).center(column_width +2) for element in columns)
        #     columns_formatted = "|" + columns_formatted + "|"
        #     horizontal_lines = "-" * (len(columns_formatted))

        #     # Print column section
        #     print(horizontal_lines)
        #     print(columns_formatted)
        #     print(horizontal_lines)

        #     # Print rows
        #     for row in data:
        #         row = "|".join(str(element).center(column_width + 2) for element in row)
        #         row = "|" + row + "|"
        #         print(row)
        #     print("\n")
        pass

    def alter_cmd(self):
        """
        
        These statement will look very similar to SQL, but format is going to be changed to help
        reduce parsing complexity.
        The typical formats:
            alter table <name> drop <a_name>;
            alter table <name> add <a_name> <a_type>;
            alter table <name> add <a_name> <a_type> default <value>;
        
        Lets look at each part:
            • alter table: All DDL statements that start with this will be considered to be trying
            to alter a table. Both are considered to be keys words.
            • <name>: is the name of the table to alter. All table names are unique.
            • drop <a name> version: will remove the attribute with the given name from the table;
            including its data. drop is a keyword.
            • <name> add <a name> <a type> version: will add an attribute with the given name
            and data type to the table; as long as an attribute with that name does not exist
            already. It will then will add a null value for that attribute to all existing tuples in the
            database. add is a keyword.
            • <name> add <a name> <a type> default <value>: version: will add an attribute
            with the given name and data type to the table; as long as an attribute with that name
            does not exist already. It will then will add the default value for that attribute to all
            existing tuples in the database. The data type of the value must match that of the
            attribute, or its an error. default is a keyword.
        Any attribute being dropped cannot be the primary key.
        Examples:
        alter table foo drop bar;
        alter table foo add gar double;
        alter table foo add far double default 10.1;
        alter table foo add zar varchar(20) default "hello world";
        Note: altering a table is not just as easy as removing/adding an attribute. For example,
        things like number of records per page need to be modified.

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """

        status = self.process_simple_cmds()
        if status == 1:
            return BAD_STATUS

        return GOOD_STATUS

    def delete_cmd(self):
        """
        These statements will look very similar to SQL, but the format is going to be changed to
        help reduce parsing complexity.
        The typical format:
        delete from <name> where <condition>;
        Lets look at each part:
            • delete from: All DML statements that start with this will be considered to be trying
            to delete data from a table. They both are to be considered keywords.
            • <name>: is the name of the table to delete from. All table names are unique.
            • where <condition>: A condition where a tuple should deleted. If this evaluates to
            true the tuple is remove; otherwise it remains. See below for evaluating conditionals. If
            there is no where clause it is considered to be a where true and all tuples get deleted.
            where is considered a keyword.
        Example:
            delete from foo;
            delete from foo where bar = 10;
            delete from foo where bar > 10 and foo = "baz";
            delete from foo where bar != bazzle;
        If a value being deleted is referred to by another table via a foreign key the delete will not
        happen and an error will be reported.
        Upon error the deletion process will stop. Any items deleted before the error will still be
        deleted

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """

        status = self.process_simple_cmds()
        if status == 1:
            return BAD_STATUS
        
        return GOOD_STATUS

    def update_cmd(self):
        """
        These statements will look very similar to SQL, but the format is going to be changed to
        help reduce parsing complexity.
        The typical format:
        update <name>
        set <column_1> = <value>
        where <condition>;
        Lets look at each part:
            • update: All DML statements that start with this will be considered to be trying to
            update data in a table. Keyword.
            • <name>: is the name of the table to update in. All table names are unique.
            • set <column 1> = <value> Sets the column to the provided values. set is a key-
            word.
            • <value>: a constant value.
            • where <condition>: A condition where a tuple should updated. If this evaluates to
            true the tuple is updated; otherwise it remains the same. See below for evaluating
            conditionals. If there is no where clause it is considered to be a where true and all
            tuples get updated.
        Example:
        update foo set bar = 5 where baz < 3.2;
        update foo set bar = 1.1 where a = "foo" and bar > 2;
        Records should be changed one at a time. If an error occurs with a tuple update then the
        update stops. All changes prior to the error are still valid.

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """

        status = self.process_simple_cmds()
        if status == 1:
            return BAD_STATUS
        
        return GOOD_STATUS

    def conditional(self):
        """
        Conditionals can be a single relational operation or a list of relational operators separated
        by and / or operators. and / or follow standard computer science definitions:
        • <a> and <b>: only true if both a and b are true.
        • <a> or <b>: only true if either a or b are true.
        and has a higher precedence than or. Items of the same precedence will be evaluated from
        left to right.

        This project will only support a subset of the relational operators of SQL:
        • = : if the two values are equal.
        • > : greater than.
        • < : less than.
        • >= : greater than or equal to.
        • <= : less than or equal to.
        • != : if the two values are not equal.

        Relational operators will return true / false values. The left side of a relational operator
        must be an attribute name; it will be replaced with its actual value at evaluation. The right
        side must be an attribute name or a constant value; no mathematics. The data types must
        be the same on both sides on the comparison.

        Returns:
            Status: GOOD_STATUS or BAD_STATUS
        """
        return GOOD_STATUS

    def process_attributes(self, str_manipulate):
        #All thats left is (hopefully) the tuples for inserting statments.
        insertValues = str_manipulate.split(",")
        attributes = []
        if insertValues[0][0] == "(":
            insertValues[0] = insertValues[0][1:]
        if insertValues[-1][-1] == ")":
            insertValues[-1] = insertValues[-1][:-1]
        for value in insertValues:
            processed_insert_values = value.split(" ")
            for i in range(len(value)):
                if i+2 > len(processed_insert_values):
                    break
                if processed_insert_values[i].count('"') == 1:
                    tempVal = [' '.join([processed_insert_values[i], processed_insert_values[i+1]])]
                    processed_insert_values[i+1] = ""
                    processed_insert_values[i] = ""
                    processed_insert_values = self.insert_into_array(processed_insert_values, i, tempVal)
                    processed_insert_values = self.remove_blank_entries(processed_insert_values)
            attributes.append(processed_insert_values)
        return attributes

    def insert_into_array(self, arr, index, arr_to_insert):
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

    def remove_blank_entries(self, passedArray):
        """
        Remove blank strings from array entry

        Args:
            passedArray (arr): input list of commands

        Returns:
            array: cleaned input list
        """
        return [element for element in passedArray if element != "" if element != " "]

    def does_table_exist(self, table_name):
        does_exist = self.cat.table_exists(table_name)
        if does_exist == 1: # 1 meaning table does NOT exist
            print(f"No such table {table_name}")
            return BAD_STATUS
        elif does_exist == 2: # 2 meaning no catalog found
            return BAD_STATUS
        return GOOD_STATUS

    def process_where_orderby(self, str_manipulate):
        name = ""
        where = ""
        orderby = ""
        if "where" not in str_manipulate and "orderby" not in str_manipulate:
            name = str_manipulate.replace(" ", "") # Should just be the table name left, but make sure no trailing spaces
        elif "where" in str_manipulate and "orderby" not in str_manipulate:
            name = str_manipulate[:str_manipulate.index("where")].replace(" ", "")
            str_manipulate = str_manipulate[str_manipulate.index("where ") + len("where "):]
            where = str_manipulate.strip()
        elif "where" not in str_manipulate and "orderby" in str_manipulate:
            name = str_manipulate[:str_manipulate.index("orderby")].replace(" ", "")
            str_manipulate = str_manipulate[str_manipulate.index("orderby ") + len("orderby "):]
            orderby = str_manipulate.strip()
        elif "where" in str_manipulate and "orderby" in str_manipulate:
            name = str_manipulate[:str_manipulate.index("where")].replace(" ", "")
            str_manipulate = str_manipulate[str_manipulate.index("where ") + len("where "):]
            where = str_manipulate[:str_manipulate.index("orderby")]
            str_manipulate = str_manipulate[str_manipulate.index("orderby ") + len("orderby "):]
            orderby = str_manipulate.strip()
        else:
            print("Formatting error")
            return BAD_STATUS
        return name,where,orderby

    def help(self) -> int:
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
        return GOOD_STATUS

if __name__ == '__main__':
    QP = QueryProcessor("testDB", "1024", "64")
    # QP.main()
    inputString = [
                'insert into foo values ();',
                'insert into foo values (1 "foo bar" true 2.1), (3 "baz" true 4.14),(2 "bar" false 5.2), (5 "true" true null);', 
                'insert into foo values (1 "foo bar" "fubar up" varchar(7) 2.1)'
                ]
    for i in inputString:
        QP.inputString = i
        QP.process_complex_cmds()
        print(f"Input String: {i}\n--> {QP.command_args}\n")
    # print(f"Exit Code: {QP.main()}")
