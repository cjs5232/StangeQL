INT_BYTE_MAX_LEN = 7
INT_BYTE_TYPE = "big"

with open("test3.bin", "wb+") as f:
    f.write(int.to_bytes(1, INT_BYTE_MAX_LEN, INT_BYTE_TYPE))

with open("test3.bin", "wb+") as f:
    int_to_increment = f.read(INT_BYTE_MAX_LEN)
    incremented_int = int.from_bytes(int_to_increment, INT_BYTE_TYPE) + 1
    print(int.from_bytes(int_to_increment, INT_BYTE_TYPE))
    print(incremented_int)
    #move f pointer back
    f.write(int.to_bytes(incremented_int, INT_BYTE_MAX_LEN, INT_BYTE_TYPE))
