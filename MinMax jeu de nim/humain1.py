import nim as jeu

#Q.7
def joue(situation):
    '''
    Annonce les coups possibles, Propose au joueur de choisir son coup, Vérifie que le coup est autorisé, sinon utiliser un appel récursif,Renvoie le coup joué.
    :param situation: (int) Nombre d'alumettes en jeu
    '''
    #alumettes = jeu.coups_possibles(situation)
    print("Vous pouvez prendre:",jeu.coups_possibles(situation),"alumette(s)")
    coup = input("Combien en prennez-vous ? ")
    if int(coup) in jeu.coups_possibles(situation):
        print("")
        print("Le joueur humain 1 a choisi:", coup)
        return int(coup)
    else:
        print("Interdit")
        return joue(situation)
