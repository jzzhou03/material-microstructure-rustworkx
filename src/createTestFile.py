import random


def makeTest(x, y, z):
    with open("tests/" + str(x) + "x" + str(y) + "x" + str(z) + ".txt", "w") as file:
        file.write(str(x) + " " + str(y) + " " + str(z) + "\n")
        for i in range(z):
            for j in range(y):
                for k in range(x):
                    if j < y/2:
                        file.write(str(1) + " ")
                    else:
                        file.write(str(0) + " ")
                file.write("\n")

makeTest(1000, 1000, 1000)