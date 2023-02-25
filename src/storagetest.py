INT_BYTE_MAX_LEN = 7
INT_BYTE_TYPE = "big"


def bytes_to_int(byteRepresentation):
    return int.from_bytes(byteRepresentation, INT_BYTE_TYPE)



# with open("test2.bin", "wb+") as f:
#     f.write(int.to_bytes(True))
#     print(int.to_bytes(True))
#     floatone=14
#     f.write(floatone.to_bytes(INT_BYTE_MAX_LEN,INT_BYTE_TYPE))
#     floattwo=7
#     f.write(floattwo.to_bytes(INT_BYTE_MAX_LEN,INT_BYTE_TYPE))

# with open("test2.bin", "rb") as f:
#     value = bytes_to_int(f.read(1))
#     match value:
#         case 0:
#             print("False")
#         case 1:
#             print("True")


#     binfloatone = f.read(INT_BYTE_MAX_LEN)
#     print(binfloatone)
#     floatone = int.from_bytes(binfloatone, INT_BYTE_TYPE)
#     print(floatone)
#     binfloattwo = f.read(INT_BYTE_MAX_LEN)
#     floattwo = int.from_bytes(binfloattwo, INT_BYTE_TYPE)
#     value = float(str(floatone) + "." + str(floattwo))
#     print(value)

with open("test3.bin", "wb+") as f:
    f.write(int.to_bytes(1, INT_BYTE_MAX_LEN, INT_BYTE_TYPE))
    f.write(int.to_bytes(1, INT_BYTE_MAX_LEN, INT_BYTE_TYPE))
    f.write(int.to_bytes(True, INT_BYTE_MAX_LEN, INT_BYTE_TYPE))
