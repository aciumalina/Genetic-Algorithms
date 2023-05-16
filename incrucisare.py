def incrucisare(c1, c2, i):
    if i == 0:
        c1, c2 = c2, c1
    else:
        aux = c1
        c1 = c1[:i] + c2[i:]
        c2 = c2[:i] + aux[i:]
    return c1, c2
# l = int(input())
# c1 = input()
# c2 = input()
# index = int(input())
#
# incrucisare(c1, c2, index)