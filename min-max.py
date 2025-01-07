from IA import *

def min_max(pl, grille, id_game):
    '''
    :param pl: (str) joueur à simuler, B, Y, R ou G
    :param grille: (matrice 20x20) matrice de jeu
    :param id_game: id de la game
    :return: coup à faire selon l'algo de min_max, de la forme (num_piece, x, y, rot, isFlipped)
    '''
    # Cherche le nombre de pièce qu'il reste au joueur, pour déterminer le nombre maximal de coups que l'on peut encore jouer
    joueurs=['B', 'Y', 'R', 'G']
    pls_Plist=[]
    coups_poss_pl=[]
    for i in range(len(joueurs)):
        pls_Plist.append(piece_res(id_game, joueurs[i]))
        coups_poss_pl.append(liste_coup_possible(id_game, joueurs[i]))
        if joueurs[i]==pl:
            pl_nb=i
    # Création de l'arbre des coups possibles par le même algorithme que monte carlo
    arbre=arbre_de_coups(pl, pl_nb, grille, pls_Plist, len(pls_Plist[pl_nb]), coups_poss_pl)
    #-----analyse de l'arbre-----
    score=score_max(arbre, pl)
    smax=score[i]
    imax=[0]
    # Récupère les indices des branches qui mènent au score le plus élevé
    for i in range(1, len(score)):
        if score[i]>smax:
            smax=score[i]
            imax=[i]
        elif score[i]==smax:
            imax.append(i)
    if len(imax)==1:
        return arbre[imax[0]][0]
    else:
        # Si des parties différentes renvoient au même score le plus élevé, on cherche la partie, parmis elles, qui renvoie les scores les moins élevés pour les adversaires
        adv_imin=[]
        for i in range(len(imax)):
            jmin=[]
            for j in range (len(joueurs)):
                if j!=pl_nb:
                    jmin.append(score_min(arbre[imax[i]]))
            k=0
            for j in jmin:
                k+=j
            adv_imin.append((k,i))
        pmin=adv_imin[0][0]
        p=[adv_imin[0][1]]
        for i in range (1, len(adv_imin-1)):
            if adv_imin[i][0]<pmin:
                pmin=adv_imin[i][0]
                p=[adv_imin[i][1]]
            elif adv_imin[i][0]==pmin:
                p.append(adv_imin[i][1])
        if len(pmin)==1:
            return arbre[pmin[0]][0]
        else:
            return arbre[pmin[random.randint(0, len(pmin)-1)]][0]

def score_max(arbre, nb_pl):
    '''
    :param arbre: arbre des coups possibles
    :param nb_pl: (int) indice du joueur B=0, Y=1, R=2, G=3
    :return: (int) score maximum possible suivant cet arbre
    '''
    lst_score=[]
    for i in range (len(arbre)):
        coup, ss_arbre, lst_aPlist=arbre[i]
        if ss_arbre!=[]:
            lst_score.append(score_max(ss_arbre, nb_pl))
        else:
            lst_score.append(score_bis(coup[0], lst_aPlist[nb_pl]))
    return max(lst_score)

def score_min(arbre, nb_pl):
    '''
    :param arbre: arbre des coups possibles
    :param nb_pl: (int) indice du joueur B=0, Y=1, R=2, G=3
    :return: (int) score minimal possible suivant cet arbre
    '''
    lst_score=[]
    for i in range (len(arbre)):
        coup, ss_arbre, lst_aPlist=arbre[i]
        if ss_arbre!=[]:
            lst_score.append(score_min(ss_arbre, nb_pl))
        else:
            lst_score.append(score_bis(coup[0], lst_aPlist[nb_pl]))
    return min(lst_score)

def score_bis (id_pi_last, Plist):
    '''
    :param id_pi_last: id de la dernière pièce posée
    :param Plist: liste des pièces restantes du joueur
    :return: score final du joueur dont on a donné la liste des pièces restantes
    '''
    score=0
    if Plist==[]:
        score+=15
    else:
        for i in Plist:
            score -= taille_piece(i)
    if id_pi_last=='P1':
        score +=5
    return score