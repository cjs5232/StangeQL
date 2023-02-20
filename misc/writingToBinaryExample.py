import random
with open("testBinaryFile", "wb+") as f:
    for i in range(100):
        randInt = bytes(random.randint(1,100))
        f.write(randInt) # Writing ints
        print(randInt)
    f.write(b"this is a test string") # Writing strings

