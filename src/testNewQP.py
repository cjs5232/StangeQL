import newQP

def test_processing():
    toTest = [
        "create table tableTest(units integer primarykey, x integer, y integer primarykey)",
        "create table tableTest(units integer)",
        "create table tableTest(units integer primarykey, baz boolean, bar varchar(7) x integer, y integer)",
        "create table tableTest(units integer primarykey)",

        "select * from fakeTable;",
        "select fakeCol from tableTest",
        "select * from tableTest;",
        "select units, baz, bar from tableTest;",
        "select * from tableTest where x = 1;",
        "select * from tableTest orderby x;",
        "select * from tableTest where y = 2 and x = 1 orderby y;",

        "insert into tableTest values();",
        "insert into tableTest ();"
    ]
    expectedValues = [
        "1", # Error duplicate primarykeys
        "1", # Error no primary keys
        "0", # Table created
        "1", # Error duplicate table
        
        "1", # Error no table found
        "1", # No column fakeCol found in tableTest? is this right expected val?
        "{'name': 'tableTest', 'select': ['*'], 'where': [], 'orderby': ''}",
        "{'name': 'tableTest', 'select': ['units', 'baz', 'bar'], 'where': [], 'orderby': ''}",
        "{'name': 'tableTest', 'select': ['*'], 'where': 'x = 1', 'orderby': ''}",
        "{'name': 'tableTest', 'select': ['*'], 'where': [], 'orderby': 'x'}",
        "{'name': 'tableTest', 'select': ['*'], 'where': 'y = 2 and x = 1 ', 'orderby': 'y'}",

        "1", # Error can't insert empty values
        "1", # Error no value keyword found

    ]
    for i in range(len(toTest)):
        print(f"Testing {toTest[i]}")
        output = str(newQP.processInput(toTest[i]))
        if output == expectedValues[i]:
            print("Passed\n")
        else:
            print(f"Expected: {expectedValues[i]}")
            print(f"Actual:   {output}")

if __name__ == '__main__':
    test_processing()