# Genetic-Algorithms
Implementați un algoritm genetic pentru determinarea maximului unei funcții pozitive pe un domeniu dat. Funcția va fi un polinom de gradul 2, cu coeficienți dați. Algoritmul trebuie să cuprindă etapele de selecție, încrucișare (crossover) și mutație.

Date de intrare • Dimensiunea populației (numărul de cromozomi) • Domeniul de definiție al funcției (capetele unui interval închis) • Parametrii pentru funcția de maximizat (coeficienții polinomului de grad 2) • Precizia cu care se lucrează (cu care se discretizează intervalul) • Probabilitatea de recombinare (crossover, încrucișare) • Probabilitatea de mutație • Numărul de etape al algoritmului

Conținut fișier de ieșire În fișier vor fi incluse cel puțin următoarele informații: • Populația inițială, cu următoarele date pentru fiecare individ i: – Bi , reprezentarea pe biți a cromozomului; – Xi , valoarea corespunzătoare cromozomului în domeniul de definiție al funcției (număr real);

– f (Xi), valoarea cromozomului, adică valoarea funcției în punc- tul din domeniu care corespunde acestuia.

• Probabilitățile de selecție pentru fiecare cromozom

• Probabilitățile cumulate care dau intervalele pentru selecție

• Evidențierea procesului de selecție, care constă în generarea unui număr aleator u uniform pe [0, 1) și determinarea intervalului [qi, qi+1) căruia aparține acest număr; corespunzător acestui in- terval se va selecta cromozomul i + 1. Procesul se repetă până se

selectează numărul dorit de cromozomi. Cerință: căutarea intervalului corespunzător se va face folosind căutarea binară. • Evidențierea cromozomilor care participă la recombinare.

• Pentru recombinările care au loc se evidențiază perechile de cro- mozomi care participă la recombinare, punctul de rupere generat

aleator precum și cromozomii rezultați în urma recombinării (sau, după caz, se evidențiază tipul de încrucișare ales).

• Populația rezultată după recombinare. • Populația rezultată după mutațiile aleatoare. • Pentru restul generațiilor (populațiile din etapele următoare) se

va afișa doar valoarea maximă și valoarea mediei a fitness- ului (performanței) populației
