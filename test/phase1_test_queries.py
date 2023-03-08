"display schema;" # No tables to display SUCCESS

"display info foo;" # No such table foo ERROR

"select * from foo;" # No such table foo ERROR

'insert into foo values (1 "foo";)' # No such table foo ERROR

"create table foo( num integer);" # No primary key defined ERROR

"create table foo( num integer primarykey);" # SUCCESS

"display info foo;" # <output> SUCCESS

"display schema;" # <output> SUCCESS

"select * from foo;" # <output>

"insert into foo values (1),(2);" # SUCCESS

"insert into foo values (3,2);" # row (3.2): Invalid data type: expected (integer) got (double). ERROR

"insert into foo values (1 3.2);" # row (1 3.2): Too many attributes: expected (integer) got (integer double) ERROR

"select * from foo;" # <output> SUCCESS

"insert into foo values (3),(1),(4);" # row (1): Duplicate primary key for row (1) ERROR

"select * from foo;" # <output> SUCCESS

"display info foo;" # <output> SUCCESS

"<quit>" # <output> + end session + on restart resume from where left off w/ correct output

"display schema;" # <output> SUCCESS

"select * from foo;" # <output> SUCCESS

"create table foo( x double primarykey, y char(5));" # Table of name foo already exists ERROR

"create table bar( x double primarykey, y char(5));" # SUCCESS

"create table bar2( double x primarykey, y char(5));" # Invalid data type "x" ERROR

"display schema;" # <output> SUCCESS

"create table bar2( x double primarykey, x char(5));" # Duplicate attribute name "x" ERROR

"create table bar2( x double primarykey, y char(5) primarykey);" # More than one primarykey ERROR

"create table bar2();" # Table with no attributes ERROR

"create table bar2( x double, y char(5) primarykey);" # SUCCESS

'insert into bar values (3.2 "helloworld");' # row (3.2 "helloworld"): char(5) can only accept 5 chars; "helloworld" is 10 ERROR

'insert into bar values (3.2 "hello"), (14.5 "a23ab"), ("hello" 3.2);' # row ("hello", 3.2): Invalid data types: expected (double char(5)) got (char(5) double) ERROR

"select * from bar" # <output> SUCCESS

'insert into bar2 values (3.2 "hello"), (14.5 "a23ab");'

"select * from bar2;" # <output> SUCCESS

"<quit>" # <output> exit