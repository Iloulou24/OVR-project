from math import sqrt
'''si pas précisé les tuples peuvent être remplacée pas de listes'''

def même_longueur(point,liste_de_points):
    '''
    modifie les coordonnées d'un point en rajoutant des dimensions(0)
    Arguments :
        point:Tuples (1,2) ou liste [1,2]
        liste de points : liste de tuples avec leur classe et les coordonnées
        [
        ([1,2,3,4],"A"),
        ([4,3,2,1],"B")]

    Retourne :
        le point (en tuple) est la liste de point de même dimension
    '''
    if type(point) == tuple:
        point=list(point)
    while len(point)!=len(liste_de_points[1][0]):
        if len(point)<len(liste_de_points[1][0]):
            point.append(0)
        else:
            for i in range (len(liste_de_points)):
                liste_de_points[i][0].append(0)
    return tuple(point),liste_de_points




def distance_euclidienne(point_a,point_b):
    ''' Retourne la distance euclidienne entre deux points.
        Les points sont représentés par des tuples ou des listes de nombres.
        Le nombre de dimensions doit être le même pour les deux points.
        Arguments :
            point_a (tuple ou list) : Premier point.
            point_b (tuple ou list) : Deuxième point.
        Retourne :
            float : La distance euclidienne entre point_a et point_b.
    '''
    somme_carre=0
    for i in range(len(point_a)):
        difference_au_carre=(point_a[i]-point_b[i])**2
        somme_carre+=difference_au_carre
    return sqrt(somme_carre)



def trouver_k_plus_proches_voisins(point_cible,donnees_entrainement,k):
    '''trouve les k points les plus proches du point cible en fonction
       d'une liste de points donnée
       Argument:
           point_cible: tuple d'entiers
           donnees_entrainement : liste de point avec leur classe
           k: nombre de voisins à trouver
       Retourne:
            list: Une liste des k tuples (point, classe) représentant les voisins les plus proches.
    '''
    liste_distance=[]
    for i in range (len(donnees_entrainement)):
        liste_distance.append((distance_euclidienne(point_cible,donnees_entrainement[i][0]),donnees_entrainement[i]))
    liste_distance.sort()
    liste_k_voisins=[liste_distance[i][1] for i in range(k)]
    return liste_k_voisins




def vote(voisins):
    ''' trouve le nombre de fois qu'une classe est dans la liste
        et déterminer laquelle est majoritaire
        Argument:
            voisins : liste de tuples
        Retourne:
            classe majoritaire : caractère
    '''
    dico_voisin={}
    for v in voisins:
        if v[1] in dico_voisin:
            dico_voisin[v[1]]+=1
        else :
            dico_voisin[v[1]]=1
    return max(dico_voisin, key=dico_voisin.get)





def determiner_classe(point_cible,donnees_entrainement,k):
    voisins = trouver_k_plus_proches_voisins(point_cible,donnees_entrainement,k)
    return vote(voisins),k


