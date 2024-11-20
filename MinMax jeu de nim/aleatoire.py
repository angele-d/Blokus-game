import nim as jeu
import random

def joue(situation):
    '''
    Annonce les coups possibles, Choisit un coup aléatoire, Vérifie que le coup est autorisé, sinon utiliser un appel récursif,Renvoie le coup joué.
    :param situation: (int) Nombre d'alumettes en jeu
    '''
    #alumettes = jeu.coups_possibles(situation)
    print("Vous pouvez prendre:",jeu.coups_possibles(situation),"alumette(s)")
    coup = random.choice(jeu.coups_possibles(situation))
    print("")
    print("Le bot aléatoire a choisi: ", coup)
    return int(coup)