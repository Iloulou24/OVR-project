# -*- coding: utf-8 -*-
from perceptron_multidimension_plib import *
from K_NN_plib import*
import matplotlib.pyplot as plt
import numpy as np  # couleurs jusqu'à 10 classes
cmap = plt.get_cmap('tab10')

dataset_test = [
    # Classe 0 (centre ~ (1,1))
    ((0.8, 1.1), 0),
    ((1.2, 0.9), 0),
    ((1.0, 1.3), 0),
    ((1.4, 1.1), 0),
    ((0.7, 0.8), 0),
    ((1.6, 1.4), 0),
    ((1.3, 0.6), 0),
    ((0.9, 1.7), 0),
    ((1.8, 1.2), 0),
    ((1.1, 0.7), 0),

    # Classe 1 (centre ~ (5,5))
    ((4.8, 5.1), 1),
    ((5.2, 4.9), 1),
    ((5.0, 5.4), 1),
    ((5.6, 5.2), 1),
    ((4.7, 4.6), 1),
    ((5.8, 5.6), 1),
    ((5.3, 4.4), 1),
    ((4.9, 5.8), 1),
    ((6.0, 5.1), 1),
    ((5.1, 4.7), 1),

    # Classe 2 (centre ~ (9,9))
    ((8.8, 9.1), 2),
    ((9.2, 8.9), 2),
    ((9.0, 9.4), 2),
    ((9.6, 9.2), 2),
    ((8.7, 8.6), 2),
    ((9.8, 9.6), 2),
    ((9.3, 8.4), 2),
    ((8.9, 9.8), 2),
    ((10.0, 9.1), 2),
    ((9.1, 8.7), 2),

    # Classe 3 (centre ~ (3,8))
    ((2.8, 8.1), 3),
    ((3.2, 7.9), 3),
    ((3.0, 8.4), 3),
    ((3.6, 8.2), 3),
    ((2.7, 7.6), 3),
    ((3.8, 8.6), 3),
    ((3.3, 7.4), 3),
    ((2.9, 8.8), 3),
    ((4.0, 8.1), 3),
    ((3.1, 7.7), 3),

    # Classe 4 (centre ~ (7,2))
    ((6.8, 2.1), 4),
    ((7.2, 1.9), 4),
    ((7.0, 2.4), 4),
    ((7.6, 2.2), 4),
    ((6.7, 1.6), 4),
    ((7.8, 2.6), 4),
    ((7.3, 1.4), 4),
    ((6.9, 2.8), 4),
    ((8.0, 2.1), 4),
    ((7.1, 1.7), 4),
]


def intialisation_KNN(point_cherche,données):
    print("tentative avec le K-NN")
    k=int(input(f"combien de proche voisin? Max {len(dataset_test)} "))
    while k > len(dataset_test):
        k=int(input(f"nombre pas valide, entrez un nombre valide (Max{len (dataset_test)})"))
    return determiner_classe(point_cherche,données,k)


def deux_classes(data_set,c):
    ''' transforme un dataset multiclasse en un datataset deux classes
        Arguments:
         data_set:dataset multiclasse
         classe_s: classe à garder
        retourne:
         dataset séparée en deux classes (1:classe c et 0:autres classes)
    '''
    dc_dataset=[]
    for p in data_set:
        x=p[0]
        if p[1]==c:
            y=1
        else:
            y=0
        dc_dataset.append([x,y])
    return dc_dataset

dico_dataset={}
class_max=0
for i in range(len(dataset_test)):
    if dataset_test[i][1]>class_max:
        class_max=dataset_test[i][1]
class_max=class_max+1

#un dataset différent pour chaque classe:
for i in range(class_max):
    dico_dataset["dataset",i] = deux_classes(dataset_test, i)


#un perceptron différent pour chaque classe
perceptrons = {
    i : {"w": (0,0,0), "b": 0, "success": "none"} for i in range(class_max)}

learning_rate = 1

#entrainement de pour chaque perceptron:
for d in range(class_max):
    train=entrainement(dico_dataset[('dataset',d)],perceptrons[d]["w"],perceptrons[d]["b"],learning_rate)
    w,b,succès=train[0],train[1],train[2]
    perceptrons[d] = {"w": list(w), "b": b, "success": succès}


point=input("entrez des données de même longueur que celle des données essayées")
point=point.strip("()").split(",")
point=[float(i) for i in point]



liste_score=[]

#stockage de chaque score de chaque perceptron pour le point essayé
for c in range(len(perceptrons)):
    score=predire(point, perceptrons[c]["w"], perceptrons[c]["b"])[1]
    liste_score.append(score)
    
meilleur_score=liste_score[0] # ne pas choisir un nombre aléatoire (même 0)
classe=0                      # car les scores pourraient être inferieur au nombre choisi

for i in range (len(liste_score)):
    if liste_score[i]>meilleur_score:
        meilleur_score=liste_score[i]
        classe=i

liste_score.sort(reverse=True)
delta_score=liste_score[0]-liste_score[1]

if meilleur_score <= 0 or delta_score <= 0.2 * abs(liste_score[0]):#teste la précision des perceptron
    result_KNN = intialisation_KNN(point, dataset_test)
    print(f"La classe du point est {result_KNN[0]}")
    voisins=trouver_k_plus_proches_voisins(point,dataset_test,result_KNN[1])
    
    # Tous les points du dataset
    for (x, y), classe in dataset_test:
        plt.scatter(x, y, color=cmap(classe), alpha=0.5)

    # k plus proches voisins
    for (x, y), classe in voisins:
        plt.scatter(x, y, color=cmap(classe), edgecolors='black', s=150)

        # Ligne vers le point testé
        plt.plot([point[0], x], [point[1], y], linestyle='dotted', color='gray')

    # Point testé
    plt.scatter(point[0], point[1], color='red', marker='x', s=200)

    plt.title(f"K-NN (k={result_KNN[1]})")
    plt.show()






else:
    print(f"Le point appartient à la classe {classe}")
#***REPRESENTATION GRAPHIQUE EN DEUX DIMENTIONS(si seulement x1 et x2 max)***
    if len(point) == 2:
        x_vals = np.linspace(0, 10, 100)

        for c in range(class_max):
            w = perceptrons[c]["w"]
            b = perceptrons[c]["b"]

            if w[1] != 0:
                y_vals = -(w[0] * x_vals + b) / w[1]
                plt.plot(x_vals, y_vals, label=f"Classe {c}")
            else:
                x = -b / w[0]
                plt.axvline(x, label=f"Classe {c}")



        for (x, y), c in dataset_test:
            plt.scatter(x, y, color=cmap(c))

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Données 2D par classe")

        # Point testé
        plt.scatter(point[0], point[1], marker='x', s=100)

        plt.legend()
        plt.show()
    
