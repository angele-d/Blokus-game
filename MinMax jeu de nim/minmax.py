import nim as jeu
import time

def minmax(situation, profondeur, joueur):
    coups_possibles = jeu.coups_possibles(situation)
    
    if jeu.est_fini(situation) or profondeur == 0:
        return (0, evaluer(situation, joueur))
    else:
        situations_suivantes = [ jeu.maj_situation(situation, coup) for coup in coups_possibles ]        
        if joueur == 'minmax':            
            res = max_tuple( [ minmax(situation_suivante, profondeur - 1, 'ADVERSAIRE') for situation_suivante in situations_suivantes ] )
        else:
            res = min_tuple( [ minmax(situation_suivante, profondeur - 1, 'minmax') for situation_suivante in situations_suivantes ] )       
        return (coups_possibles[res[0]],res[1])

def max_tuple(tab):
    '''
    Renvoie un tuple formé de deux nombres :
    1 : indice du tuple qui a la plus grande valeur en deuxième position
    2 : la valeur de ce maximum
    :param tab: (list) liste de tuple contenant des couples d'entier
    :return: (tuple)
    >>> max_tuple([(1, 0), (2, 0), (3, 10)])
    (2, 10)
    '''
    indice_mx = 0
    mx = tab[0][1]
    for j in range(1,len(tab)):
        if tab[j][1] > mx:
            mx = tab[j][1]
            indice_mx = j
    return (indice_mx, mx)

def min_tuple(tab):
    '''
    Renvoie un tuple formé de deux nombres :
    1 : indice du tuple qui a la plus petite valeur en deuxième position
    2 : la valeur de ce minimum
    :param tab: (list) liste de tuple contenant des couples d'entier
    :return: (tuple)
    >>> min_tuple([(1, -10), (2, 0), (3, 0)])
    (0, -10)
    '''
    indice_mn = 0
    mn = tab[0][1]
    for j in range(1,len(tab)):
        if tab[j][1] < mn:
            mn = tab[j][1]
            indice_mn = j
    return (indice_mn, mn)

def evaluer(situation, joueur):
    '''
    Renvoie un score en fonction de la situation et du joueur :
    Si on est en situation d'un jeu fini : renvoyer 10 si le joueur est minmax -10 sinon
    Sinon renvoyer 0        
    '''
    if jeu.est_fini(situation):
        if joueur == "minmax": #le paramètre joueur correspond au joueur suivant
            return 10
        else:
            return -10
    else:
        return 0

def joue(situation):
    '''
    Annonce les coups possibles, Choisit un coup aléatoire, Vérifie que le coup est autorisé, sinon utiliser un appel récursif,Renvoie le coup joué.
    :param situation: (int) Nombre d'alumettes en jeu
    '''
    #alumettes = jeu.coups_possibles(situation)
    print("Vous pouvez prendre:",jeu.coups_possibles(situation),"alumette(s)")
    coup = (minmax(situation, 10, "minmax"))[0]
    print("")
    print("Le champion MinMax a choisi: ", coup)
    return int(coup)

