"""
CSCI.421 - Database System Implementation

File: test.py
Authors:
    - Gunnar Bachmann (ggb6130)
    - Aidan Mellin (atm3232)
    - Alex Cooley (arc7311)
    - Cindy Donch (cad7046)
    - Connor Stange (cjs5232)
"""

binToType = {
    b'001': "<class 'int'>",
    b'010': "<class 'float'>", 
    b'011': "<class 'str'>", #Varchar and char will have to be str
    b'100': "<class 'bool'>"
}

typeToBin = {}
for i in binToType:
    typeToBin[binToType[i]] = i

# print(typeToBin)

INT_BYTE_MAX_LEN = 7
INT_BYTE_TYPE = "big"
TYPE_LEN = 3

with open("test.bin", "wb+") as f:
    valuesWeWantToAdd = (1199, "hi", True, 10.14) # values we want to figure out how to write to file
    floatEncoded = str(valuesWeWantToAdd[3]).split(".") #Encode the String

    castArray = []
    for i in floatEncoded:
        castArray.append(int(i).to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE))
    print(castArray)

    encodedValues = []

    encodedValues.append()

    
    
    
    encodedLength = len(floatEncoded).to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE)

    encodedValues = [typeToBin[str(type(valuesWeWantToAdd[3]))], encodedLength, floatEncoded]
    for i in encodedValues:
        f.write(i)

with open("test.bin", "rb") as f:
    type = f.read(TYPE_LEN)
    print(type)
    print(binToType[type])
    knownInt = f.read(INT_BYTE_MAX_LEN)
    knownInt = int.from_bytes(knownInt, INT_BYTE_TYPE)
    print(knownInt)
    knownString = f.read(knownInt)
    print(knownString.decode())


def write_and_read_int_from_file():
    with open("test.bin", "wb+") as f:
        valuesWeWantToAdd = (1199, "hi", True) # values we want to figure out how to write to file
        
        intEncoded = valuesWeWantToAdd[0].to_bytes(INT_BYTE_MAX_LEN,INT_BYTE_TYPE) #Encode the int

        print(f"int Encoded: {intEncoded}")
        # print(f"int decoded: {int.from_bytes(intEncoded,INT_BYTE_TYPE)}")

        encodedValues = [typeToBin[str(type(valuesWeWantToAdd[0]))], intEncoded]
        for i in encodedValues:
            f.write(i)

    with open("test.bin", "rb") as f:
        type = f.read(TYPE_LEN)
        print(type)
        print(binToType[type])
        knownInt = f.read(INT_BYTE_MAX_LEN)
        print(knownInt)
        print(int.from_bytes(knownInt, INT_BYTE_TYPE))

def write_string(string):
    with open("test.bin", "wb+") as f:
        #encode string to account for special characters
        stringEncoded = string.encode()
        #get the byte length of the string we are writing
        encodedLength = len(stringEncoded).to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE)
        f.write(encodedLength)
        f.write(stringEncoded)

        encodedValues = [typeToBin[str(type(valuesWeWantToAdd[1]))], encodedLength, stringEncoded]
        for i in encodedValues:
            f.write(i)

    pass





def write_and_read_string_from_file():
    with open("test.bin", "wb+") as f:
        valuesWeWantToAdd = (1199, "hi", True) # values we want to figure out how to write to file
        
        stringEncoded = valuesWeWantToAdd[1].encode() #Encode the String

        encodedLength = len(stringEncoded).to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE)

        encodedValues = [typeToBin[str(type(valuesWeWantToAdd[1]))], encodedLength, stringEncoded]
        for i in encodedValues:
            f.write(i)

    with open("test.bin", "rb") as f:
        type = f.read(TYPE_LEN)
        print(type)
        print(binToType[type])
        knownInt = f.read(INT_BYTE_MAX_LEN)
        knownInt = int.from_bytes(knownInt, INT_BYTE_TYPE)
        print(knownInt)
        knownString = f.read(knownInt)
        print(knownString.decode())

def write_and_read_bool_from_file():
    with open("test.bin", "wb+") as f:
        valuesWeWantToAdd = (1199, "hi", True) # values we want to figure out how to write to file
        
        stringEncoded = str(valuesWeWantToAdd[2]).encode() #Encode the String

        encodedLength = len(stringEncoded).to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE)

        encodedValues = [typeToBin[str(type(valuesWeWantToAdd[2]))], encodedLength, stringEncoded]
        for i in encodedValues:
            f.write(i)

    with open("test.bin", "rb") as f:
        type = f.read(TYPE_LEN)
        print(type)
        print(binToType[type])
        knownInt = f.read(INT_BYTE_MAX_LEN)
        knownInt = int.from_bytes(knownInt, INT_BYTE_TYPE)
        print(knownInt)
        knownString = f.read(knownInt)
        print(knownString.decode())
        
def bool_rw():
    with open("test2.bin", "wb+") as f:
        f.write(int.to_bytes(True))
        print(int.to_bytes(True))

    with open("test2.bin", "rb") as f:
        value = f.read(1)
        value = int.from_bytes(value, INT_BYTE_TYPE)
        match value:
            case 0:
                print("False")
            case 1:
                print("True")

def double_rw():
    with open("test2.bin", "wb+") as f:
        floatone=14
        f.write(floatone.to_bytes(INT_BYTE_MAX_LEN,INT_BYTE_TYPE))
        floattwo=7
        f.write(floattwo.to_bytes(INT_BYTE_MAX_LEN,INT_BYTE_TYPE))

    with open("test2.bin", "rb") as f:
        binfloatone = f.read(INT_BYTE_MAX_LEN)
        print(binfloatone)
        floatone = int.from_bytes(binfloatone, INT_BYTE_TYPE)
        print(floatone)
        binfloattwo = f.read(INT_BYTE_MAX_LEN)
        floattwo = int.from_bytes(binfloattwo, INT_BYTE_TYPE)
        value = float(str(floatone) + "." + str(floattwo))
        print(value)