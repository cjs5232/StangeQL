INT_BYTE_MAX_LEN = 7
INT_BYTE_TYPE = "big"

with open("test3.bin", "wb+") as f:
    int_to_write = 20
    print(int_to_write.to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE))
    f.write(int_to_write.to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE))

with open("test3.bin", "rb+") as f:
    num_pages_pointer = f
    int_to_increment = f.read(INT_BYTE_MAX_LEN)
    print(int_to_increment)
    incremented_int = int.from_bytes(int_to_increment, INT_BYTE_TYPE) + 1
    print(int.from_bytes(int_to_increment, INT_BYTE_TYPE))
    print(incremented_int)
    #move f pointer back
    neg = 0 - INT_BYTE_MAX_LEN
    f.seek(neg,1)
    print(incremented_int.to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE))
    num_pages_pointer.write(incremented_int.to_bytes(INT_BYTE_MAX_LEN, INT_BYTE_TYPE))

with open("test3.bin", "rb+") as f:
    incremented_int = f.read(INT_BYTE_MAX_LEN)
    incremented_int = int.from_bytes(incremented_int, INT_BYTE_TYPE)
    print(incremented_int)
