from fonc_DB import *
import random

def arbre_de_coups(pl, grille, adv_Plist, n):
    '''
    Fonction qui genère l'arbre des coups possibles
    :param pl: (str) B,G,Y,R = joueur
    :param grille: matrice 20x20
    :param adv_Plist: liste des pièces de tous les joueurs [BPlist, YPlist, RPlist, GPlist]
    :param n: (int) nombre de coups à simuler, profondeur de l'arbre des coups (nb de coups du joueur pl)
    :return: arbre des coups de la forme [(coup, [liste des coups suivants ce coup], [liste des pièces des différents joueurs au niveau de ce coup])]'''
    arbre=[]
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
                suite=coups_adversaires(List_aPlist, [grille2], pl, pl) #renvoie liste des coups de la forme [(liste des grilles après coups, liste des pièces rstantes des joueurs)]
                ss_arbre=[] #construction du sous-arbre
                for j in suite:
                    ss_arbre.append(arbre_de_coups(pl, j[0], j[1], n-1))
                arbre.append((coup, ss_arbre, List_aPlist))
            return arbre

def coups_adversaires(List_aPlist, Lcoups, pl, m):
    '''
    Fonction qui renvoie toutes les grilles correspondantes à tous les coups possibles des adversaires
    :param List_aPlist: liste des pièces restantes des joueurs, sous la force [LpiècesB, LpiècesY, LpiècesR, LpiècesG]
    :param Lcoups: liste des coups à renvoyer (liste de grilles, liste des pièces)
    :param pl: (str) B, Y, R, G = joueur simulé par IA
    :param m: (int) dernier joueur à avoir posé une pièce
    :return: liste des grilles suite aux coups des adversaires et la mise à jour des listes des pièces des joueurs, sous la forme lst[([grilles], [lst_pieces_joueurs])]
    '''
    #Si c'est au tour du joueur dont on simule les coups, on arrête là
    if pl=='B':
        if m=='G':
            return (Lcoups, List_aPlist)
    if pl=='Y':
        if m=='B':
            return (Lcoups, List_aPlist)
    if pl=='R':
        if m=='Y':
            return (Lcoups, List_aPlist)
    if pl=='G':
        if m=='R':
            return (Lcoups, List_aPlist)
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
                            L2=List_aPlist.copy()
                            for k in range(len(L2[0])):
                                if L2[0][k]==j[0]:
                                    L2[0].pop(k)
                            Lcoups2.append(j,L2)
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
                            L2=List_aPlist.copy()
                            for k in range(len(L2[1])):
                                if L2[1][k]==j[0]:
                                    L2[1].pop(k)
                            Lcoups2.append(j,L2)
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
                            L2=List_aPlist.copy()
                            for k in range(len(L2[2])):
                                if L2[2][k]==j[0]:
                                    L2[2].pop(k)
                            Lcoups2.append(j,L2)
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
                            L2=List_aPlist.copy()
                            for k in range(len(L2[3])):
                                if L2[3][k]==j[0]:
                                    L2[3].pop(k)
                            Lcoups2.append(j,L2)
            return coups_adversaires(List_aPlist, Lcoups2, pl, 'G')

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
    #récupération listes des pièces restantes de chaque joueur + indice correspondant au joueur IA
    for i in range(len(joueurs)):
        pls_Plist.append(piece_res(id_game, joueurs[i]))
        if joueurs[i]==pl:
            pl_nb=i
    #création des arbres de coups possibles
    arbre=arbre_de_coups(pl, grille, pls_Plist, n, [])
    if len(arbre)==1:
        return arbre[0][0]
    #on détermine si des coups ammènent à des profondeurs moins fortes
    profondeurs=[]
    for i in arbre:
        profondeurs.append(profondeur_ac(i[1]))
    #ensiute on cherche à éliminer les coups avec les plus faibles profondeurs (les coups amenant à des fins de parties)
    prof_max=max(profondeurs)
    arbre2=[]
    for i in range(len(profondeurs)):
        if profondeurs[i]==prof_max:
            arbre2.append(arbre[i])
    if len(arbre2)==1:
        return arbre[0][0]
    #on cherche ensuite les coups qui utilisent les pièces les plus grandes
    tailles_pi=[]
    for i in range (len(arbre2)):
        tailles_pi.append(taille_piece_arbre(arbre2[i][1]))
    taille_max=max(tailles_pi)
    arbre=[]
    for i in range(len(tailles_pi)):
        if taille_max==tailles_pi[i]:
            arbre.append(arbre2[i])
    if len(arbre)==1:
        return arbre[0][0]
    #on cherche maintenant à déterminer les coups qui bloquent le plus les adversaires, ie les branches où les adversaires ont le moins de coups possibles
    arbre2=[]
    min_coup_adv=nb_coups_adv(grille, arbre, pl_nb, pls_Plist) #de la forme [(adv, minimum de coup de l'adv, liste des coups qui y mènent)]
    #si on a un seul adversaire, on garde tous les coups menant à ce minimum
    if len(min_coup_adv)==1:
        for i in range (len(arbre)): #[(coup,ss-arbre, lst_pieces_joueurs)]
            if arbre[i][0] in min_coup_adv[0][2]:
                arbre2.append(arbre[i])
    #sinon, si on a 2 adversaires
    elif len(min_coup_adv)==2:
        #on regarde si il y des coups qui mènent aux deux minimums
        cpareils=[]
        for i in min_coup_adv[0][2]:
            for j in min_coup_adv[1][2]:
                if i==j:
                    cpareils.append(i)
        if cpareils!=[]:
            for i in range(len(arbre)):
                if arbre[i][0] in cpareils:
                    arbre2.append(arbre[i])
        else:
            #si aucun coup n'est en commun, on les ajoute tous
            for i in range (len(arbre)):
                if arbre[i][0] in min_coup_adv[0][2] or arbre[i][0] in min_coup_adv[1][2]:
                    arbre2.append(arbre[i])
    else:
        #si on a 3 adversaires
        #on regarde d'abord si des coups sont commun aux trois minimums
        cpareils=[]
        for i in min_coup_adv[0][2]:
            for j in min_coup_adv[1][2]:
                for k in min_coup_adv[2][2]:
                    if i==j and j==k:
                        cpareils.append(i)
        if cpareils!=[]:
            for i in range(len(arbre)):
                if arbre[i][0] in cpareils:
                    arbre2.append(arbre[i])
        else:
            #sinon, on regarde si des coups sont commun à au moins deux minimums
            for i in min_coup_adv[0][2]:
                for j in min_coup_adv[1][2]:
                    for k in min_coup_adv[2][2]:
                        if i==j or j==k or i==k:
                            cpareils.append(i)
            if cpareils!=[]:
                for i in range(len(arbre)):
                    if arbre[i][0] in cpareils:
                        arbre2.append(arbre[i])
            else:
                #si aucun chemin n'est en commun, on les ajoute tous
                for i in range (len(arbre)):
                    if (arbre[i][0] in min_coup_adv[0][2]) or (arbre[i][0] in min_coup_adv[1][2]) or (arbre[i][0] in min_coup_adv[2][2]):
                        arbre2.append(arbre[i])
    if len(arbre2)==1:
        return arbre2[0][0]
    else:
        petit_carre=True
        for i in range (len(arbre2)):
            if arbre2[i][0][0]!=P1:
                petit_carre=False
                break
        #si on ne commence que pas l'utilisation d'un petit carré
        if petit_carre:
            return arbre2[random.randint(0, len(arbre2)-1)][0]
        #sinon
        else:
            for i in range(len(arbre2)):
                if arbre2[i][0][0]==P1:
                    arbre2.pop(i)
            return arbre2[random.randint(0, len(arbre2)-1)][0]
                    

def profondeur_ac(arbre):
    '''
    :param arbre: arbre des coups, de la forme list[(coup, sous-arbre, lst_pieces_joueurs)]
    :return: (int) profondeur max de l'arbre
    '''
    if arbre==[]:
        return 0
    else:
        m=[]
        for i in range (len(arbre)):
            m.append(1+profondeur_ac(arbre[i][1]))
    return max(m)

def taille_piece(pi):
    '''
    :param pi: (str) id de la pièce
    :return: nombre de cases dont la pièce est composée
    '''
    res=0
    for i in range (5):
        for j in range (5):
            if pi[i][j]:
                res+=1
    return res

def taille_piece_arbre(arbre):
    '''
    :param n: (int) nombre de cases des autres pièces de l'arbre
    :param arbre: arbre dont la taille totale de toutes les pièces utilisées est à calculer de la forme list[(coup, ss-arbre, lst_pieces_joueurs)]
    :return: (int) nombre de cases totale pour toutes les pièces utilisées
    '''
    if arbre==[]:
        return 0
    else:
        m=[]
        for i in range (len(arbre)):
            m.append(taille_piece(arbre[i][0][0])+taille_piece_arbre(arbre[i][1]))
    return max(m)

def nb_coups_adv(grille, arbre, pl_nb, pls_Plist):
    '''
    :param grille: matrice 20x20 de jeu, à la base de l'arbre
    :param arbre: arbre de coups de la forme list[(coup, ss-arbre, lst_pieces_joueurs)]
    :param pl: (str) B, Y, R, G = joueur 
    :param pl_nb: indice du joueur IA
    :param pls_Plist: liste de toutes les pièces restantes des joueurs
    :return: le nombre de coups minimal de chaque adversaires ainsi que les coups à la racine de l'arbre qui y conduisent de la forme [(adv, minimum de coup de l'adv, liste des coups qui y mènent)]
    '''
    joueurs=['B', 'Y', 'R', 'G']
    res=[0,0,0,0]
    res[pl_nb]=-1 #on met à -1 ce qui correspond au joueur ia
    for i in range (len(pls_Plist)):
        if pls_Plist[i]==[]:
            res[i]=-2 #on met à -2 ce qui correspond à aucun joueur
    coups_min_adv=[]
    for i in range (len(res)):
        if res[i]!=-1 and res[i]!=-2:
            coups_min_adv.append(nb_coup_arbre(arbre, grille, joueurs[i], pls_Plist[i]))
    return coups_min_adv

def nb_coup_arbre(arbre, grille, pl, Plist):
    '''
    :param arbre: arbre des coups list[(coup,ss-arbre, lst_pieces_joueurs)] #coup de la forme (pi, x, y, rot, isflipped)
    :param grille: matrice 20x20 de jeu
    :param pl: (str) B, Y, R, G = joueur
    :param Plist: (lst) liste des pièces restantes du joueur pl
    :return: (int) le nombre de coups minimal du joueur pl par les coups de l'arbre, et la liste des coups à la racine de l'arbre emmenant à ce minimum
    '''
    if arbre==[]:
        return len(coups_possibles_force_brute(grille, pl, Plist))
    else:
        colo=['B', 'Y', 'R', 'G']
        for i in range(len(colo)):
            if pl==colo[i]:
                nb_pl=i
        m=[]
        for i in range (len(arbre)):
            m.append(nb_coup_arbre(arbre[i][1], placer_piece_grille20x20(grille, arbre[i][0][0], arbre[i][0][1], arbre[i][0][2], pl, arbre[i][0][3], arbre[i][0][4] ), pl, arbre[i][2][nb_pl]))
        cmin=[]
        mini=min(m)
        for i in range(len(arbre)):
            if m[i]==mini:
                cmin.append(arbre[i][0])
        return (pl, mini, cmin)