import math

def calcul_nr_biti(a,b,p):
    return math.ceil(math.log2((b-a) * pow(10, p)))

def calcul_pas_discretizare(a,b,l):
    return (b-a)/pow(2,l)

def codificare(nr,a,l,d):
    interval = math.floor((nr-a)/d)
    cod = ""
    for i in range(l):
        cod += str(interval % 2)
        interval //= 2
    cod = cod[::-1]
    return cod

def interval_decodificare(nr):
    putere = len(nr) - 1
    numar = 0
    for bit in nr:
        numar += int(bit) * pow(2, putere)
        putere -= 1
    return numar

def capat_interval(interval, a,d):
    return "{0:.7f}".format(a + interval * d)

# a,b = [int(x) for x in input().split()]
# p = int(input())
# m = int(input())
# words = []
# for i in range(2*m):
#     words.append(input())

# l = calcul_nr_biti(a,b,p)
# d = calcul_pas_discretizare(a,b,l)

# for i, value in enumerate(words):
#     if value == 'TO':
#         codificare(float(words[i+1]))
#     elif value == 'FROM':
#         interval = interval_decodificare(words[i+1])
#         capat_interval(interval)
