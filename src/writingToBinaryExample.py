import random
with open("testBinaryFile", "wb+") as f:
    for i in range(100):
        f.write(bytes(random.randint(1,100)))
    f.write(b"this is a test string")

