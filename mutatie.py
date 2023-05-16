def mutatie(cromozom, pozitii):
    cromozom_aux = [x for x in cromozom]
    for i in pozitii:
        if cromozom_aux[i] == '0':
            cromozom_aux[i] = '1'
        else:
            cromozom_aux[i] = '0'
    return ''.join(cromozom_aux)

# l, k = [int(x) for x in input().split()]
# # cromozom = input()
# # pozitii = [int(x) for x in input().split()]
# #
# # mutatie(cromozom, pozitii)