import time

#Q. 1
def regle():
    '''
    Imprime dans la console les règles du jeu
    '''
    print("Jeu de Nim: \n On dispose d’un tas d’allumette, \n Chacun son tour, un joueur prend 1, 2 ou 3 allumette(s), \n Le joueur qui prend la dernière allumette a perdu.")
    time.sleep(2)

#Q.2
def situation_initiale():
    '''
    Demande le nombre d'alumette et le stock
    :effet_de_bord: Impression dans la console
    '''
    situation = input("Nombre d'alumettes: ")
    return int(situation)

#Q.3
def affiche(situation):
    '''
    Affiche dans la console un visuel des alumettes restantes
    :param situation: (int)
    '''
    for i in range (situation):
        print ("| " ,end='')
    print ('(',situation,')')

#Q.4
def est_fini(situation):
    '''
    Renvoie True si la partie est finie et False sinon
    :param situation: (int)
    '''
    return situation == 0

#Q.5
def coups_possibles(situation):
    '''
    Renvoie un tuple contenant les coups possibles pour le joueur
    :param situation: (int)
    '''
    if int(situation) <= 3:
        return tuple(i for i in range(1,situation+1))
    else: #situation >3
        return (1,2,3)

#Q.6
def maj_situation(situation,coup):
    '''
    Renvoie la nouvelle situation en prenant en compte le coup qui vient d'être joué
    :param situation: (int)
    :param coup: (int)
    '''
    return situation-coup


