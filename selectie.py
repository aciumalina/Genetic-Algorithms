def calcul_functie(a,b,c,x):
    return (a * (x**2) + b * x + c)

def calcul_valori_fitness(a,b,c,cromozomi):
    fitness = []
    for crom in cromozomi:
        fitness.append(calcul_functie(a,b,c,crom))
    return fitness

def calcul_fitness_total(fitness):
    return sum(fitness)

# a,b,c = [int(x) for x in input().split()]
# n = int(input())
# cromozomi = [float(x) for x in input().split()]
#
# valori_fitness = calcul_valori_fitness(cromozomi)
# F = calcul_fitness_total(valori_fitness)
# capete_interval = [0]
# suma = 0
# for val in valori_fitness:
#     suma += val
#     capete_interval.append(round(suma/F, 5))
#
# for interval in capete_interval:
#     print(interval)

