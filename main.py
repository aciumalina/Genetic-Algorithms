import codificare
import incrucisare
import mutatie
import selectie
import random
import matplotlib.pyplot as plt

def citire_date(fisier):
    with open(fisier, 'r') as fin:
        a, b, c = [int(x) for x in fin.readline().split()]
        capete = [int(x) for x in fin.readline().split()]
        dimensiune = int(fin.readline().rstrip())
        precizie = int(fin.readline().rstrip())
        p_recombinare = float(fin.readline().rstrip())
        p_mutatie = float(fin.readline().rstrip())
        etape = int(fin.readline().rstrip())

    return a, b, c, capete[0], capete[1], dimensiune, precizie, p_recombinare, p_mutatie, etape

#generare primi indivizi ai populatiei
def genereaza_nr_aleator(a_capat, b_capat, precizie=0, dimensiune_pop=0):
    pop = []
    for i in range(dimensiune_pop):
        numar_aleator = round(random.uniform(a_capat, b_capat), precizie)
        pop.append(numar_aleator)
    return pop

#trec succesiv prin fitness-urile tuturor cromozomilor, le adun la suma curenta, impart la fitness total
#capetele intervalului vor fi mereu 0 si 1
def calcul_intervale_selectie(total, valori_functie):
    capete_interval = [0]
    suma = 0
    for val in valori_functie:
        suma += val
        capete_interval.append(suma / total)
    return capete_interval


def afisare_prob_selectie(valori_functie, printare = True):
    if printare:
        print("Probabilitati selectie ", file = fout)
    #calculez suma fitness-urilor
    total = selectie.calcul_fitness_total(valori_functie)
    for i, val in enumerate(valori_functie):
        p = val / total
        if printare:
            print(f'cromozom {i + 1} probabilitate {p}', file = fout)

    intervale_selectie = calcul_intervale_selectie(total, valori_functie)
    return intervale_selectie


def afisare_pop_initiala_intervale_select(pop_necodif, a_capat, l, d, a, b, c, printare = True):
    if printare:
        print("Populatia initiala: ", file = fout)
    valori_functie = []
    pop_codificata = []
    #trec prin indivizii generati aleator, care acum sunt float-uri, si le generez codificarea si le calculez fitness-ul
    for idx, nr in enumerate(pop_necodif):
        cod = codificare.codificare(nr, a_capat, l, d)
        pop_codificata.append(cod)
        valoare_functie = selectie.calcul_functie(a, b, c, nr)
        valori_functie.append(valoare_functie)
        idx += 1
        if printare:
            print(f"{idx}: {cod} x= {nr}, f={valoare_functie}", file = fout)

    #tot aici calculez si probabilitatea lor de selectie si intervalele de selectie
    intervale_selectie = afisare_prob_selectie(valori_functie, printare = printare)

    if printare:
        print("Intervale selectie", file = fout)
        print(intervale_selectie, file = fout)

    return intervale_selectie, pop_codificata, valori_functie


def cautare_binara(intervale_selectie, val, start, end):
    if start == end:
        if intervale_selectie[start] > val:
            return start
        else:
            return start + 1
    if start > end:
        return start

    mid = (start + end) // 2
    if intervale_selectie[mid] < val:
        return cautare_binara(intervale_selectie, val, mid + 1, end)
    elif intervale_selectie[mid] > val:
        return cautare_binara(intervale_selectie, val, start, mid - 1)
    else:
        return mid


def proces_selectie(intervale_selectie, dimensiune_pop, printare = True):
    cromozomi_selectati = []
    #selectare cromozomilor in functie de u generat aleator
    for i in range(dimensiune_pop):
        u = random.uniform(0, 1)
        #caut intervalul in care se afla, prin cautare binara
        index = cautare_binara(intervale_selectie, u, 0, len(intervale_selectie) - 1)
        if printare:
            print(f'u= {u} selectam cromozomul {index}', file=fout)
        cromozomi_selectati.append(index)
    return cromozomi_selectati


def afisare_dupa_selectie(cromozomi_selectati, populatie_codificata, populatie_necodificata, valori_functie, printare = True):
    if printare:
        print("Dupa selectie: ", file = fout)
    populatie_codificata_nou = []
    populatie_necodificata_nou = []
    valori_functie_nou = []
    count = 0
    for index in cromozomi_selectati:
        count += 1
        if printare:
            print(
            f"{count}: {populatie_codificata[index - 1]} x= {populatie_necodificata[index - 1]}, f={valori_functie[index - 1]}", file = fout)
        #actualizarea populatiei, pastrand doar indivizii care au fost selectati
        populatie_codificata_nou.append(populatie_codificata[index - 1])
        populatie_necodificata_nou.append(populatie_necodificata[index - 1])
        valori_functie_nou.append(valori_functie[index - 1])
    return populatie_codificata_nou, populatie_necodificata_nou, valori_functie_nou


def selectie_cromozomi_incrucisare(cromozomi_selectati_codificati, p_recombinare, dimensiune_pop, printare = True):
    if printare:
        print('Probabilitatea de incrucisare', p_recombinare, file = fout)
    count = 0
    cromozomi_de_incrucisat = []
    #pentru fiecare individ ii generez un u aleator, in functie de care decid daca el participa la recombinare sau nu
    for i in range(dimensiune_pop):
        u = random.uniform(0, 1)
        count += 1
        if u < p_recombinare:
            if printare:
                print(f"{count}: {cromozomi_selectati_codificati[i]} u= {u} < {p_recombinare} participa", file = fout)
            #adaugarea lui in lista de cromozomi de incrucisat
            cromozomi_de_incrucisat.append((cromozomi_selectati_codificati[i], i))
        else:
            if printare:
                print(f"{count}: {cromozomi_selectati_codificati[i]} u= {u}", file = fout)
    return cromozomi_de_incrucisat


def calcul_cromozomi_dupa_incrucisare(cromozomi_de_incrucisat, populatie_necodificata, populatie_codificata,
                                      valori_functie, a, b, c, a_capat, d, printare = True):
    # lista cromozomi_de_incrucisat contine tupluri unde primul element e cromozomul si al doilea
    # element este indexul lui in lista initiala de cromozomi
    # in aceasta functie, dupa recombinare, schimb si valorile din populatia codificata/necodificata si valorile functiei in punctele respective

    # sortez lista descrescator in functie de fitness, pentru a ii grupa 2 cate 2
    cromozomi_de_incrucisat.sort(key=lambda x: valori_functie[x[1]])

    for i in range(0, len(cromozomi_de_incrucisat) - 1, 2):
        cromozom1, index1 = cromozomi_de_incrucisat[i]
        cromozom2, index2 = cromozomi_de_incrucisat[i + 1]
        # generare pozitie rupere
        pozitie_rupere = random.randint(0, len(cromozom1))
        if printare:
            print(f"Recombinare dintre cromozom {index1 + 1} cu cromozom {index2 + 1}", file = fout)
            print(cromozom1, cromozom2, "punct", pozitie_rupere, end=" ", file = fout)
        cromozom_nou1, cromozom_nou2 = incrucisare.incrucisare(cromozom1, cromozom2, pozitie_rupere)
        if printare:
            print("\nRezultat ", cromozom_nou1, cromozom_nou2, file = fout)
            print(file = fout)

        # inlocuirea vechilor cromozomi cu cei noi, actualizare codificari si fitness-uri
        populatie_codificata[index1] = cromozom_nou1
        populatie_codificata[index2] = cromozom_nou2

        populatie_necodificata[index1] = float(
            codificare.capat_interval(codificare.interval_decodificare(cromozom_nou1), a_capat, d))
        populatie_necodificata[index2] = float(
            codificare.capat_interval(codificare.interval_decodificare(cromozom_nou2), a_capat, d))

        valori_functie[index1] = selectie.calcul_functie(a, b, c, populatie_necodificata[index1])
        valori_functie[index2] = selectie.calcul_functie(a, b, c, populatie_necodificata[index2])


    return populatie_necodificata, populatie_codificata, valori_functie

def print_status_dupa_recombinare(populatie_necodificata, populatie_codificata, valori_functie, printare = True):
    #printare status dupa recombinare, trec prin toate codificarile, indivizii si fitness-urile lor
    count = 0
    print("Dupa recombinare:", file = fout)
    for i in range(len(valori_functie)):
        count += 1
        print(f"{count}: {populatie_codificata[i]}, x = {populatie_necodificata[i]}, f= {valori_functie[i]}", file = fout)


def print_status_mutatie(p_mutatie, populatie_necodificata, populatie_codificata, valori_functie, a, b, c, a_capat, d, printare = True):
    if printare:
        print('Probabilitate de mutatie pentru fiecare gena', p_mutatie, file = fout)
        print("Au fost modificati cromozomii: ", file = fout)
    #trec prin toti cromozomii si prin toate genele lor, stiu ca fiecare gena are o anumita
    #probbabilitate de mutatie si generez cate un u pentru fiecare
    for index_cromozom, cromozom in enumerate(populatie_codificata):
        for i in range(len(cromozom)):
            u = random.uniform(0, 1)
            if u > 0.01:
                continue
            #altfel am gasit o gena de alterat
            if printare:
                print(index_cromozom+1, file=fout)

            #mutarea cromozomului
            cromozom_dupa_mutatie = mutatie.mutatie(populatie_codificata[index_cromozom], [i])

            #pentru noul cromozom rezultat, ii calculez si actualizez noile metrici
            populatie_codificata[index_cromozom] = cromozom_dupa_mutatie

            populatie_necodificata[index_cromozom] = float(
                codificare.capat_interval(codificare.interval_decodificare(cromozom_dupa_mutatie), a_capat, d))

            valori_functie[index_cromozom] = selectie.calcul_functie(a, b, c, populatie_necodificata[index_cromozom])

    if printare:
        count = 0
        for index in range(len(valori_functie)):
            count += 1
            print(
                f"{count}: {populatie_codificata[index]} x= {populatie_necodificata[index]}, f={valori_functie[index]}", file = fout)
    return populatie_necodificata, populatie_codificata, valori_functie

def status_evolutie_maxim(valori_functie, etapa):
    #printare max fitness si mean fitness
    maxim = max(valori_functie)
    media = sum(valori_functie)/len(valori_functie)
    print("Etapa", etapa, file = fout)
    print('Max fitness:', maxim, file = fout)
    print('Mean fitness:', media, file = fout)
    print(file=fout)

    return etapa, maxim, media

def plotare(etape, maxime, medii):
    plt.plot(etape, maxime, color='r', label='Fitness maxim')
    plt.plot(etape, medii, color='g', label='Media fitness')
    plt.show()

def main():
    nr_etape = []
    #listele unde voi introduce valorile de max fitness si mean fitness pentru plotare
    maxime = []
    medii = []

    printare = True

    #citirea datelor de intrare din fisier
    a, b, c, a_capat, b_capat, dimensiune_pop, precizie, p_recombinare, p_mutatie, etape = citire_date('input.in')
    #generarea populatiei initiale
    populatie_necodificata = genereaza_nr_aleator(a_capat, b_capat, precizie, dimensiune_pop)
    #calcul nr de biti necesari pentru reprezentarea cromozomilor
    l = codificare.calcul_nr_biti(a_capat, b_capat, precizie)
    #calcul pas discretizare
    d = codificare.calcul_pas_discretizare(a_capat, b_capat, l)
    #calculul intervalelor de selectie, codificarea populatiei si calcularea fitnessului pentru toti indivizii
    intervale_selectie, populatie_codificata, valori_functie = afisare_pop_initiala_intervale_select(
        populatie_necodificata, a_capat, l, d, a, b, c)

    #calculez metricile celui mai bun individ din generatie
    best_fitness = max(valori_functie)
    index_individ_best_fitness = valori_functie.index(best_fitness)
    cod_individ_best_fitness = populatie_codificata[index_individ_best_fitness]
    individ_best_fitness = populatie_necodificata[index_individ_best_fitness]

    #selectarea cromozomilor
    cromozomi_selectati = proces_selectie(intervale_selectie, dimensiune_pop)
    #actualizarea metricilor populatiei dupa selectie
    populatie_codificata, populatie_necodificata, valori_functie = afisare_dupa_selectie(cromozomi_selectati,
                                                                                         populatie_codificata,
                                                                                         populatie_necodificata,
                                                                                         valori_functie)
    #generarea cromozomilor care participa la recombinare
    cromozomi_de_incrucisat = selectie_cromozomi_incrucisare(populatie_codificata, p_recombinare, dimensiune_pop)
    #actualizarea metricilor populatiei dupa recombinare
    populatie_necodificata, populatie_codificata, valori_functie = calcul_cromozomi_dupa_incrucisare(
        cromozomi_de_incrucisat, populatie_necodificata, populatie_codificata, valori_functie, a, b, c, a_capat, d)
    #printare situatiei actuale, dupa recombinare
    print_status_dupa_recombinare(populatie_necodificata, populatie_codificata, valori_functie)
    #actualizarea metricilor populatiei dupa mutatiile aleatoare
    populatie_necodificata, populatie_codificata, valori_functie = print_status_mutatie(p_mutatie, populatie_necodificata, populatie_codificata, valori_functie, a, b, c, a_capat, d)

    #trecerea celui mai bun individ in etapa urmatoare
    if individ_best_fitness not in populatie_necodificata:
        individ_de_inlocuit = valori_functie.index(min(valori_functie))
        populatie_necodificata[individ_de_inlocuit] = individ_best_fitness
        populatie_codificata[individ_de_inlocuit] = cod_individ_best_fitness
        valori_functie[individ_de_inlocuit] = best_fitness

    #evolutia fitnessului
    nr_etapa, maxim, medie = status_evolutie_maxim(valori_functie, 1)

    nr_etape.append(nr_etapa)
    maxime.append(maxim)
    medii.append(medie)

    printare = False

    #repetarea procesului pentru numarul ramas de etape, insa fara printare in fisier
    for i in range(1,etape):
        intervale_selectie, populatie_codificata, valori_functie = afisare_pop_initiala_intervale_select(
            populatie_necodificata, a_capat, l, d, a, b, c, printare=False)
        # valorile celui mai bun individ din generatie
        best_fitness = max(valori_functie)
        index_individ_best_fitness = valori_functie.index(best_fitness)
        cod_individ_best_fitness = populatie_codificata[index_individ_best_fitness]
        individ_best_fitness = populatie_necodificata[index_individ_best_fitness]

        cromozomi_selectati = proces_selectie(intervale_selectie, dimensiune_pop, printare = False)
        populatie_codificata, populatie_necodificata, valori_functie = afisare_dupa_selectie(cromozomi_selectati,
                                                                                             populatie_codificata,
                                                                                             populatie_necodificata,
                                                                                             valori_functie, printare = False)
        cromozomi_de_incrucisat = selectie_cromozomi_incrucisare(populatie_codificata, p_recombinare, dimensiune_pop, printare = False)
        populatie_necodificata, populatie_codificata, valori_functie = calcul_cromozomi_dupa_incrucisare(
            cromozomi_de_incrucisat, populatie_necodificata, populatie_codificata, valori_functie, a, b, c, a_capat, d, printare = False)
        populatie_necodificata, populatie_codificata, valori_functie = print_status_mutatie(p_mutatie,
                                                                                            populatie_necodificata,
                                                                                            populatie_codificata,
                                                                                            valori_functie, a, b, c,
                                                                                            a_capat, d, printare = False)
        if individ_best_fitness not in populatie_necodificata:
            individ_de_inlocuit = valori_functie.index(min(valori_functie))
            populatie_necodificata[individ_de_inlocuit] = individ_best_fitness
            populatie_codificata[individ_de_inlocuit] = cod_individ_best_fitness
            valori_functie[individ_de_inlocuit] = best_fitness

        nr_etapa, maxim, medie = status_evolutie_maxim(valori_functie, i+1)

        nr_etape.append(nr_etapa)
        maxime.append(maxim)
        medii.append(medie)

    plotare(nr_etape, maxime, medii)


if __name__ == '__main__':
    with open('Evolutie.txt', 'w') as fout:
        main()
