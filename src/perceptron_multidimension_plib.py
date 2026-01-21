def predire(x, w, b):
    '''prédit le classe d'un point en fonction de ses coordonnées,
       du poids de chacun des coordonnées et d'un biais
       Arguments:
        x:coordonnées:tuple ou liste d'entiers
        w:poids (même longueur que x)
        biais:(entier)
       Retourne:
        prédiction de la classe du point
    '''
    S=0
    for i  in range(len(x)):
        S += x[i]*w[i]
    S+=b
    prediction = 1 if S>0 else 0
    return prediction,S

def modif_poids(x, prediction, vrai_résultat, w, b, learning_rate):
    '''modifie la valeur des poids
       arguments:
        x :coordonnées:tuple ou liste d'entiers
        prediction (1 ou 0)
        vrai_résultat: (1 ou 0)
        w: poids (même longueur que x)
        b: biais:(entier)
        learning_rate:vitesse d'apprentissage(entier)
       retourne:
        les poids et le biais corrigés (tuple dans un tuple)
    '''
    w=list(w)
    erreur = vrai_résultat-prediction
    for i in range (len(x)):
        w[i]+=learning_rate*erreur*x[i]
    b+=learning_rate*erreur
    return (tuple(w), b)

def entrainement(échantillon_de_données,w,b,learning_rate):
    '''calibre les poids pour permettre de donner un bonne prédiction en fonctiondes échantillons données
       arguments:
        échantillon_de_données: liste de points (en tuple) avec leur coordonnées + leur classe
        ((x1,x2,x3),classe) ex: ((1,2,6,9),1 ou 0)
        w: poids pour chaque coordonée (tuple ou liste d'entiers)
        b: biais (entier)
        learning_rate : entier
       retourne:
        poids et biais calibrés (tuples)
    '''
    nb_success_epoch=0
    max_stagnation=0
    while nb_success_epoch<50 and max_stagnation<50:
        nb_success=0
        for d in échantillon_de_données:
            prediction=predire(d[0],w,b)
            if prediction!=d[-1]:
                modif=modif_poids(d[0],prediction[0],d[-1],w,b,learning_rate)
                liste_ancien_poids =[i for i in w]
                liste_ancien_poids.append(b)
                w,b=modif[0],modif[1]
                liste_nouv_poids =[i for i in w]
                liste_nouv_poids.append(b)
                somme_différence=0
                for i in range(len(liste_ancien_poids)):
                    différence=abs(liste_nouv_poids[i]-liste_ancien_poids[i])
                    somme_différence+=différence
                variation_moyenne = somme_différence / len(liste_ancien_poids)
                if variation_moyenne < 0.1:
                    max_stagnation += 1
                else:
                    max_stagnation = 0

                nb_success=0
            else:
                nb_success+=1
        if nb_success<=len(échantillon_de_données):
            nb_success_epoch+=1


    return w,b,nb_success_epoch>=50
