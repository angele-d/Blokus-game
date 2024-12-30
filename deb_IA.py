from fonc_DB import *
from logique_jeu import *

#pour calculer le coup à faire, on utilise Monte carlo, avec approche probabiliste. Donc, d'une grille de jeu donnée, avec la liste des pièces restantes et le oueur qui joue
#on va simuler un arbre des coups d'une profondeur n et donner à chaque branche une proba, déterminée par le nombre de victoire et le nombre de défaites que la branch epeut créer
#Pour ce faire, on fait un fonction avec comme argument, le joueur, le nombre de jouerus, la grille, les pieces restantes
#on va devoir faire une fonction auxiliaire avec la création de l'arbre, l'analyse de celui-ci, et l'attribution des coefficients/proba des branches
#on va d'abbord se focaliser sur le milieu de partie
#pour le début, les 4 premiers tours, on va utiliser le coups_possible_début plus tard
#utliser le plus possible les grosses pièces au début, mais pas les barres, pour bloquer les adversaires

def arbre_de_coups(pl, grille, adv_Plist, n, arbre):
    '''
    Fonction qui genère l'arbre des coups possibles
    :param pl: (str) B,G,Y,R = joueur
    :param grille: matrice 20x20
    :param adv_Plist: liste des pièces de tous les joueurs [BPlist, YPlist, RPlist, GPlist]
    :param n: (int) nombre de coups à simuler, profondeur de l'arbre des coups (nb de coups du joueur pl)
    :param arbre: (list) arbre en cours de création, initialement []
    :return: arbre des coups de la forme [(coup, [liste des coups suivants ce coup])]'''
    if n==0:
        return [] #l'arbre s'arrête là
    if Plist==[]:
        return [] #l'arbre s'arrête là
    else:
        if pl=='B':
            Plist=adv_Plist[0]
        elif pl=='Y':
            Plist=adv_Plist[1]
        elif pl=='R':
            Plist=adv_Plist[2]
        else:
            Plist=adv_Plist[3]
        cr=coup_restant_force_brute(grille, pl, Plist)
        if not cr:
            return [] #il n'y a plus de coups  possible, l'arbre s'arrête là
        else:
            c_possibles=coups_possibles_force_brute(grille, pl, Plist)
            for i in range (len(c_possibles)):
                coup=c_possibles[i] #coup de la forme (pi, x, y, rot, isflipped)
                Plist2=Plist.copy()
                Plist2.pop(i)
                grille2=placer_piece_grille20x20(grille, coup[0], coup[1], coup[2], pl, coup[3], coup[4]) #mise à jour la grille avec la nouvelle pièce ajoutée 
                joueurs=['B', 'Y', 'R', 'G']
                List_aPlist=adv_Plist.copy()
                for k in len(joueurs):
                    if k==pl:
                        List_aPlist[i]=Plist2
                suite=coups_adversaires(List_aPlist, [grille2], pl, pl)
                ss_arbre=[] #construction du sous-arbre
                for j in suite:
                    ss_arbre.append(arbre_de_coups(pl, j, Plist2, n-1, []))
                arbre.append((coup, ss_arbre))
            return arbre

def coups_adversaires(List_aPlist, Lcoups, pl, m):
    '''
    Fonction qui renvoie toutes les grilles correspondantes à tous les coups possibles des adversaires
    :param List_aPlist: liste des pièces restantes des joueurs, sous la force [LpiècesB, LpiècesY, LpiècesR, LpiècesG]
    :param Lcoups: liste des coups à renvoyer (liste de grilles)
    :param pl: (str) B, Y, R, G = joueur simulé par IA
    :param m: (int) dernier joueur à avoir posé une pièce
    :return: liste des grilles suite aux coups des adversaires
    '''
    #Si c'est au tour du joueur dont on simule les coups, on arrête là
    if pl=='B':
        if m=='G':
            return Lcoups
    if pl=='Y':
        if m=='B':
            return Lcoups
    if pl=='R':
        if m=='Y':
            return Lcoups
    if pl=='G':
        if m=='R':
            return Lcoups
    #Sinon
    if m=='G':
        if List_aPlist[0]==[]:
            coups_adversaires(List_aPlist, Lcoups, pl, 'B')
        else:
            for i in Lcoups[0]:
                possible=False
                for grille in Lcoups:
                    cr=coup_restant_force_brute(grille, 'B', List_aPlist[0])
                    if cr:
                        possible=True
                        break
                if not possible:
                    coups_adversaires(List_aPlist, Lcoups, pl, 'B')
                else:
                    Lcoups2=[]
                    for grille in Lcoups2:
                        c_possibles=coups_possibles_force_brute(grille, 'B', List_aPlist[0])
                        for j in c_possibles:
                            Lcoups2.append(j)
            return coups_adversaires(List_aPlist, Lcoups2, pl, 'B')
    if m=='B':
        if List_aPlist[1]==[]:
            coups_adversaires(List_aPlist, Lcoups, pl, 'Y')
        else:
            for i in Lcoups[1]:
                possible=False
                for grille in Lcoups:
                    cr=coup_restant_force_brute(grille, 'Y', List_aPlist[1])
                    if cr:
                        possible=True
                        break
                if not possible:
                    coups_adversaires(List_aPlist, Lcoups, pl, 'Y')
                else:
                    Lcoups2=[]
                    for grille in Lcoups2:
                        c_possibles=coups_possibles_force_brute(grille, 'Y', List_aPlist[1])
                        for j in c_possibles:
                            Lcoups2.append(j)
            return coups_adversaires(List_aPlist, Lcoups2, pl, 'Y')
    if m=='Y':
        if List_aPlist[2]==[]:
            coups_adversaires(List_aPlist, Lcoups, pl, 'R')
        else:
            for i in Lcoups[2]:
                possible=False
                for grille in Lcoups:
                    cr=coup_restant_force_brute(grille, 'R', List_aPlist[2])
                    if cr:
                        possible=True
                        break
                if not possible:
                    coups_adversaires(List_aPlist, Lcoups, pl, 'R')
                else:
                    Lcoups2=[]
                    for grille in Lcoups2:
                        c_possibles=coups_possibles_force_brute(grille, 'R', List_aPlist[2])
                        for j in c_possibles:
                            Lcoups2.append(j)
            return coups_adversaires(List_aPlist, Lcoups2, pl, 'R')
    if m=='R':
        if List_aPlist[3]==[]:
            coups_adversaires(List_aPlist, Lcoups, pl, 'G')
        else:
            for i in Lcoups[3]:
                possible=False
                for grille in Lcoups:
                    cr=coup_restant_force_brute(grille, 'G', List_aPlist[3])
                    if cr:
                        possible=True
                        break
                if not possible:
                    coups_adversaires(List_aPlist, Lcoups, pl, 'G')
                else:
                    Lcoups2=[]
                    for grille in Lcoups2:
                        c_possibles=coups_possibles_force_brute(grille, 'G', List_aPlist[3])
                        for j in c_possibles:
                            Lcoups2.append(j)
            return coups_adversaires(List_aPlist, Lcoups2, pl, 'G')

def score_arbre(pl, arbre):
    '''
    Fonction qui associe à chaque branche de l'arbre un score/proba et qui permet donc de shoisir quel coups faire
    :param pl: (str) G,R,Y,B = joueur
    :arbre: (list) arbre des coups simulés
    '''
    #par exemple, le nombre de branche qui ne mène pas à une défaite/nombre de branches totales
    #trouver comment qualifier et pondérer les branches : nombres max de pièces posées, nombres d'adversaires bloqués, 
    #nombres de cases utilisées, nombre de cases restantes entre la dernière pièce posée et le cadre du jeu

def coup_a_faire(pl, grille, n, id_game):
    '''
    fonction qui donne, par la méthode Monte Carlo, le coup à faire étant donné une grille de jeu et des pièces données
    :param pl: (str) G,Y,R,B = joueur
    :param grille: matrice 20*20
    :param n: (int) profondeur d'arbre à simuler
    :param id_game: id_game
    :return: le coup à faire de la forme (num_piece, x, y, rot, isFlipped)
    '''
    joueurs=['B', 'Y', 'R', 'G']
    pls_Plist=[]
    for i in range(len(joueurs)):
        pls_Plist.append(piece_res(id_game, joueurs[i]))
        if joueurs[i]==pl:
            pl_nb=i
    

def profondeur_ac(arbre):
    '''
    :param arbre: arbre des coups, de la forme list[(coup, sous-arbre)]
    :return: (int) profondeur max de l'arbre
    '''
    if arbre==[]:
        return 0
    else:
        m=[]
        for i in range (len(arbre)):
            m.append(1+profondeur_ac(arbre[i][0]))
    return max(m)