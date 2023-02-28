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


    # def create_table_cmd(self, query:list) -> int:
    #     """
    #     Parse create table query and collect table name and attributes.
    #     Use storage manager for creating the actual table file.

    #     Creates the schema for a table. The schema is added to the catalog.
    #     The schema will be used by the system to store/access/update/delete
    #     data in the table.
    #     """
    #     try:
    #         start_idx = 3
    #         attributes = {} # Initialize dictionary to hold attributes (name, type) NOTE if key=primarykey value=column name
    #         table_name = query[2]

    #         # Steup

    #         if "()" in table_name:
    #             print("Table with no attributes")
    #             return BAD_STATUS
    #         elif "(" in table_name:
    #             split_string = table_name.split('(')
    #             query.remove(table_name)

    #             # there was a "(" + split
    #             table_name = split_string[0]
    #             query.insert(2, table_name)
    #             attr_split = split_string[1]
    #             if attr_split != '':
    #                 query.insert(3, attr_split)

    #             #table_name = table_name[:-1]

    #         elif query[start_idx] == "(":
    #             start_idx = 4


    #         # Check catalog
            # does_table_exist = self.cat.table_exists(table_name)
            # if does_table_exist == 1: # 1 meaning table does exist
            #     print(f"Table of name {table_name} already exists")
            #     return BAD_STATUS
    #         elif does_table_exist == 2: # 2 meaning no catalog found
    #             return BAD_STATUS

    #         # Loop through attributes
    #         i = start_idx
    #         while i < len(query):
    #             if query[i] == ")":
    #                 break

    #             name = query[i]
    #             if "(" in name:
    #                 name = name.strip("(")

    #             d_type = query[i+1]

    #             if "))" in d_type:
    #                 d_type = d_type[:-1]
    #             elif "char" not in d_type and "varchar" not in d_type and ")" in d_type:
    #                 d_type = d_type[:-1]

    #             if name in attributes.keys():
    #                 print(f'Duplicate attribute name "{name}"')
    #                 return BAD_STATUS

    #             if self.check_data_type(d_type) == 1:
    #                 print(f'Invalid data type "{d_type}"')
    #                 return BAD_STATUS

    #             if "," in d_type:
    #                 d_type = d_type.rstrip(',')
    #                 attributes[name] = d_type
    #                 i += 2
    #                 continue
    #             elif len(query) <= i+2:
    #                 attributes[name] = d_type
    #                 break

    #             if "primarykey" in query[i+2] and "primarykey" not in attributes.keys():
    #                 query[i+2].rstrip(',')
    #                 attributes[name] = d_type
    #                 attributes["primarykey"] = name
    #                 i += 3
    #             elif "primarykey" in query[i+2] and "primarykey" in attributes.keys():
    #                 print("More than 1 primary key")
    #                 return BAD_STATUS
    #             else:
    #                 attributes[name] = d_type
    #                 i += 2

    #         if "primarykey" not in attributes.keys():
    #             print("No primary key defined")
    #             return BAD_STATUS


    #         # {
    #         # "name" : "num",
    #         # "type" : "integer",
    #         # "primary_key" : False
    #         # }
    #         table = {
    #                 "name" : table_name,
    #                 "pageCount" : 0,
    #                 "recordCount" : 0,
    #                 "attributes" : []
    #         }

    #         for i in attributes:
    #             if not i == "primarykey": # Add all non primary keys to array of attributes in table dict
    #                 table["attributes"].append({"name" : i, "type": attributes[i], "primary_key" : False})


    #         for i in range(len(table["attributes"])):
    #             #Iterate through and find the primary key fugger
    #             if attributes["primarykey"] == table["attributes"][i]["name"]:
    #                 table["attributes"][i].update({"primary_key" : True}) # Updating to little T true in the catalog?

    #         returnCode = self.cat.add_table(table)
    #         if returnCode == 1:
    #             return BAD_STATUS

    #         status = self.StorageM.create_table(table_name)

    #         return status
    #     except:
    #         #TODO actual checks for things below
    #         #no paren around tab_name, extra parameters in the parens that arent primarykey
    #         return BAD_STATUS


    # def insert_cmd(self, query:list) -> int:
    #     """
    #     Parse the insert into query and store attributes. Use the
    #     buffer manager to physically add the tuples of data into the table.

    #     Insert tuple(s) of information into a table.
    #     """
    #     values = []
    #     table_name = query[2]
    #     query = query[4:]

    #     query_str = ' '.join(query)

    #     loop = True
    #     while loop: # Each loop builds a tuple of row values and adds tuple to values list
    #         vals = [] # list to hold each element in a row
    #         cur_val = "" # Current value being built
    #         for i in range(len(query_str)):
    #             if query_str[i] == "(" or query_str[i] == ',':
    #                 pass
    #             elif query_str[i] == ")":
    #                 if i == len(query_str) - 1:
    #                     vals.append(cur_val)
    #                     loop = False
    #                     query_str = query_str[i+1:]
    #                     break
    #                 else:
    #                     vals.append(cur_val)
    #                     query_str = query_str[i+1:]
    #                     break
    #             elif query_str[i] == ' ':
    #                 vals.append(cur_val)
    #                 cur_val = ""
    #             else:
    #                 cur_val += query_str[i]
                    
    #         values.append(tuple(vals))
        
    #     attributes = self.cat.table_attributes(table_name)
    #     if attributes == 1:
    #         return BAD_STATUS
        
    #     result = self.StorageM.insert_record(table_name, attributes, values)
    #     return result # update return based off storage manager

    def create_table_cmd(self):
        """
        Create a table in the catalog via a few steps:
        - Process complex arguments into specific arrays of attributes 
            2D Array following the form of 
            [[name of attribute type [primarykey / unique / notnull], ...]
        Check that the method of calling the command is valid:
            - Args start with create table
            - Table name passed does not already exist in the catalog
        Then iterate through the attribute array and add it to a table to be added to the catalog
            - One of the attributes passed MUST be a primarykey

        See README for more constraints on this section

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """
        status = self.process_complex_cmds()
        if status == 1:
            return BAD_STATUS

        table_name = self.command_prefix[2]

        if not ' '.join(self.command_prefix[:2]) == 'create table':
            return BAD_STATUS
        if table_name in self.keywords:
            return BAD_STATUS
        
        does_table_exist = self.cat.table_exists(table_name)
        if does_table_exist == 1:
            print(f"Table of name {table_name} already exists")
            return BAD_STATUS

        table = {
            "name" : table_name,
            "pageCount" : 0,
            "recordCount" : 0,
            "attributes" : []
        }

        tableAttribNames = [] #For easier lookup
        foundPrimaryKey = False

        #Loop through attributes
        for attrib in self.command_args:
            if len(attrib) < 2:
                print(f"Less than expected number of values <{attrib}>")
                return BAD_STATUS
            if len(attrib) > 5:
                print(f"Passed attributes more than expected values <{attrib}>")
                return BAD_STATUS
            if self.check_data_type(attrib[1]) == BAD_STATUS:
                print(f"Invalid datatype: <{attrib[1]}>")
                return BAD_STATUS
            
            if attrib[0] in tableAttribNames:
                print(f"Duplicate attribute {attrib[0]}")
                return BAD_STATUS
            
            if "primarykey" in attrib:
                foundPrimaryKey = True

            #add to table thing
            temp_Attrib = {
                "name" : attrib[0],
                "type" : attrib[1],
                "primary_key" : "primarykey" in attrib, #Technically could be in position 3, 4, or 5
                "unique" : "unique" in attrib,
                "notnull" : "notnull" in attrib
            }

            table["attributes"].append(temp_Attrib)
        
        if not foundPrimaryKey:
            print("No primary key found")
            return BAD_STATUS
        
        status = self.cat.add_table(table)

        return status
    
    def select_cmd(self):
        """
        • Each query can be one line or multiple lines.
        • The newline character is to be considered the same as a space.
        • Multiple spaces are to be considered a single space; but where spaces are shown below
        at least one space will exist there.
        • All statements will end with a semi-colon.

        (Above is for phase 3) #TODO remove this comment when implemented

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """

        status = self.process_simple_cmds()
        if status == 1:
            return BAD_STATUS
        

        return GOOD_STATUS
    
    # def select_cmd(self, query:list) -> int:
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
        
    #     return GOOD_STATUS
    
    def insert_cmd(self):
        """
        These statements will look very similar to SQL, but the format is going to be changed to
        help reduce parsing complexity.
        Be aware just like in SQL, insert will insert a new tuple and not update an existing one. If it
        tries to insert a tuple with the same primary key values as one that exists it will report an
        error and stop adding tuples. Any tuples already added will remain. Any tuple remaining to
        be added will not be added.
        The typical format:
        insert into <name> values <tuples>;
        Lets look at each part:
            • insert into: All DML statements that start with this will be considered to be trying
            to insert data into a table. Both are considered keywords.
            • <name>: is the name of the table to insert into. All table names are unique.
            • values is considered a keyword.
            • <tuples>: A space separated list of tuples. A tuple is in the form:
            ( v1 ... vN )
        Tuple values will be inserted in the order that that table attributes were created. The
        spaces/newlines after the commas are not required and added for clarity/readability.

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """
        status = self.process_complex_cmds()
        return status
    
    def drop_cmd(self):
        """
        These statement will look very similar to SQL, but format is going to be changed to help
        reduce parsing complexity. This will remove the table from the system. This includes the
        data and schema.

        The typical format:
        drop table <name>;
        Lets look at each part:
            • drop table: All DDL statements that start with this will be considered to be trying
            to drop a table. Both are considered to be keywords.
            • <name>: is the name of the table to drop. All table names are unique.

        Returns:
            status: GOOD_STATUS or BAD_STATUS
        """
        return GOOD_STATUS

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
        return GOOD_STATUS

    def display(self):
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
    
    def display_schema_cmd(self) -> int:
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

    def display_info_cmd(self, table_name:str) -> int:
        """
        Calls print_table from Catalog to print given Table Names information.
        Including: Table name, table schema, number of pages, number of records.
        All output comes from Catalog.print_table.
        """
        if self.cat.print_table(table_name) == 1:
            return BAD_STATUS # FAILURE

        return GOOD_STATUS # SUCCESS


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

    def process_input(self, query:list) -> int:
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
                    return BAD_STATUS
            else:
                return BAD_STATUS
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

    def process_complex_cmds(self):
        """
        Process passed commands for select, create, and insert statements where there are weird things with parentheses and multiple inserts being passed.

        Follows some easy steps:
        - Get rid of the prefix commands (like create table foo)
        - Join the array into one string again

        Args:
            inputString (str): passed command from user

        Returns:
            array: array of attributes to be processed.
        """
        # inputString = self.remove_blank_entries(inputString) #TODO LATER
        attribs = self.inputString.split("(")[1:]
        attribs = self.remove_blank_entries(attribs)
        attribs = ' '.join(str(x) for x in attribs).replace("char ", "char(")
        attribs = attribs.split(",")
        temp_attribs = []
        processed_attribs = []
        
        for i in attribs:
            if i == '' or i == ')':
                print(f"Error in formatting <{self.inputString}>")
                return BAD_STATUS
            if i[-1] == ")":
                i = i[:-1]
            if i[0] == " ":
                i = i[1:]
            temp_attribs.append(i)
        for processed_attrib in temp_attribs:
            processed_attrib = self.remove_blank_entries(processed_attrib.split(" "))
            processed_attribs.append(processed_attrib)

        self.command_args = processed_attribs
        return GOOD_STATUS

    def process_simple_cmds(self):
        """
        Process the simple(r) by comparison commands for select, drop, alter, delete, update where the 
        commands follow a pretty simple flow.

        Returns:
            _type_: _description_
        """
        
        '''
        Test commands
        (below command has different spacing also for testing)
        select one, two,three from foo where x = 1 and y=2 orderby x;
        drop table foo;
        alter table foo drop num;
        alter table foo add testcol boolean default False;
        delete from foo where num = 1;
        update foo set num = 1;
        '''

        print(self.inputString)
        argumentsSplit = re.split(r' |,', self.inputString)
        argumentsSplit = self.remove_blank_entries(argumentsSplit)
        # print(argumentsSplit)
        conditionalKeywords = ["=", ">", "<", ">=", "<=", "!="]
        temp = []
        for arg in argumentsSplit:
            for cond in conditionalKeywords:
                if cond in arg:
                    argSplit = arg.split("=")
                    if len(argSplit) == 2:
                        temp = [argSplit[0], cond, argSplit[1]]
        #how to remove the y=2 from list and replace with temp?
        # command_list = ["select", "drop", "alter", "delete", "update"]



        #TODO check if no spaces in conditionals and split on conditional keywords
        
        return GOOD_STATUS

    def remove_blank_entries(self, passedArray):
        """
        Remove blank strings from array entry

        Args:
            passedArray (arr): input list of commands

        Returns:
            array: cleaned input list
        """
        return [element for element in passedArray if element != ""]

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

            inputString = readInput.replace(";", "").lower()
            self.inputString = inputString
            command_prefix = inputString.split("(")[0].split(" ")
            if len(command_prefix) < 3 and "display" not in command_prefix:
                print(f"Incorrect format <{''.join(str(x) for x in readInput)}>")
                status = 1
            specificCommand = command_prefix[0]
            self.command_prefix = command_prefix
            commands = {
                "create" : lambda: self.create_table_cmd(),
                "select": lambda: self.select_cmd(),
                "insert" : lambda: self.insert_cmd(),
                "drop" : lambda: self.drop_cmd(),
                "alter" : lambda: self.alter_cmd(),
                "delete" : lambda: self.delete_cmd(),
                "update" : lambda: self.update_cmd(),
                "display" : lambda: self.display()
            }
            if status != 1:
                status = commands.get(specificCommand, lambda: "invalid")()

            # status = self.process_input(inputString)
            if status == 0:
                print("SUCCESS\n")
            else:
                print("ERROR\n")


if __name__ == '__main__':
    QP = QueryProcessor("testDB", "1024", "64")
    QP.main()
    print(f"Exit Code: {QP.main()}")
