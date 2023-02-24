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
    "001": "<class 'int'>",
    "010": "<class 'float'>", 
    "011": "<class 'str'>", #Varchar and char will have to be str
    "100": "<class 'bool'>"
}

typeToBin = {}
for i in binToType:
    typeToBin[binToType[i]] = i

# print(typeToBin)

INT_BYTE_MAX_LEN = 7
INT_BYTE_TYPE = "big"
DELIMETER = ""

with open("test.bin", "wb+") as f:
    valuesWeWantToAdd = (1199, "hi", True) # values we want to figure out how to write to file
    
    intEncoded = valuesWeWantToAdd[0].to_bytes(INT_BYTE_MAX_LEN,INT_BYTE_TYPE) #Encode the int
    stringEncoded = valuesWeWantToAdd[1].encode() #Encode the String
    boolEncoded = bytes(valuesWeWantToAdd[2])

    stringGetByteLength = bytes(len(bytearray(stringEncoded))) #Get the length of the string
    boolGetByteLength = bytes(1)

    # print(f"int Encoded: {intEncoded}")
    # print(f"int decoded: {int.from_bytes(intEncoded,INT_BYTE_TYPE)}")


    encodedValues = [typeToBin[str(type(valuesWeWantToAdd[0]))].encode(), intEncoded]
    for i in encodedValues:
        f.write(i)
        f.write(DELIMETER.encode())

    

with open("test.bin", "r") as f:
    read = f.read()
    print(read)
    maxAttribWritten = 2
    for i in read:
        print(i)