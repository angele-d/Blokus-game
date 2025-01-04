from fonc_DB import *
import random

def arbre_de_coups(pl, nb_pl, grille, adv_Plist, n, adv_coups):
    '''
    Fonction qui genère l'arbre des coups possibles
    :param pl: (str) B,G,Y,R = joueur
    :param nb_pl: (int) indice du joueur pl
    :param grille: matrice 20x20
    :param adv_Plist: liste des pièces de tous les joueurs [BPlist, YPlist, RPlist, GPlist]
    :param n: (int) nombre de coups à simuler, profondeur de l'arbre des coups (nb de coups du joueur pl)
    :param adv_coups: liste des coups possibles de chaque joueurs
    :return: arbre des coups de la forme [(coup, [liste des coups suivants ce coup], [liste des pièces des différents joueurs au niveau de ce coup])]'''
    arbre=[]
    Plist=adv_Plist[nb_pl]
    if n==0:
        return [] #l'arbre s'arrête là
    if Plist==[]:
        return [] #l'arbre s'arrête là
    if adv_coups[nb_pl]==[]:
        return [] #l'arbre s'arrête là, plus de coups possibles
    else:
        c_possibles=adv_coups[nb_pl]
        for i in range (len(c_possibles)):
            coup=c_possibles[i] #coup de la forme (pi,COLOR, x, y, rot, isflipped)
            Plist2=Plist.copy()
            Plist2.pop(i)
            grille2=placer_piece_grille20x20(grille, coup[0], coup[2], coup[3], pl, coup[4], coup[5]) #mise à jour la grille avec la nouvelle pièce ajoutée 
            joueurs=['B', 'Y', 'R', 'G']
            List_aPlist=adv_Plist.copy()
            List_aCoups=adv_coups.copy()
            for k in range(len(joueurs)):
                List_aCoups[k]=coup_enleve(grille2, List_aCoups[k])
                if joueurs[k]==pl:
                    List_aPlist[k]=Plist2
                    List_aCoups[k]=coup_rajoute(grille2, new_move(grille2, pl, coup[2], coup[3]), List_aPlist[k], pl)
            suite=coups_adversaires([(grille2, List_aPlist, List_aCoups)], pl, nb_pl, pl) #renvoie liste des coups de la forme [(liste des grilles après coups, liste des pièces rstantes des joueurs, liste des coups possibles de chaque joueurs)]
            ss_arbre=[] #construction du sous-arbre
            for j in suite:
                ss_arbre.append(arbre_de_coups(pl, nb_pl, j[0], j[1], n-1, j[2]))
            arbre.append((coup, ss_arbre, List_aPlist))
        return arbre

def coups_adversaires(Lcoups, pl, nb_pl_ia, m):
    '''
    Fonction qui renvoie toutes les grilles correspondantes à tous les coups possibles des adversaires
    :param Lcoups: liste des coups à renvoyer lst[(grille, lst[pièces de tous les joueurs], lst[coups de tous les joueurs])]
    :param pl: (str) B, Y, R, G = joueur simulé par IA
    :param nb_pl_ia: (int) indice du joueur ia qu'on simule
    :param m: (int) dernier joueur à avoir posé une pièce
    :return: liste des grilles suite aux coups des adversaires et la mise à jour des listes des pièces des joueurs, sous la forme lst[(grille, [lst_pieces_joueurs], [lst_coups_joueurs])]
    '''
    joueurs=['B', 'Y', 'R', 'G']
    #Si c'est au tour du joueur dont on simule les coups, on arrête là
    if nb_pl_ia==0 and joueurs[4]==m:
        return Lcoups
    elif joueurs[nb_pl_ia-1]==m:
        return Lcoups
    Lgrille=[]
    #Sinon
    if m=='G':
        for i in Lcoups:
            if i[2][0]!=[]: #si on a des coups possibles pour ce joueurs
                Lgrille=[]
                for j in range (len(i[2][0])): #on récupère les coups de la forme (id_piece,color,pos_x,pos_y,rot,flip)
                    if j!=[]:
                        grille2=(placer_piece_grille20x20(i[0], j[0], j[2], j[3], j[1], j[4], j[5]))
                        coup2=i[2].copy()
                        pieces2=i[1].copy()
                        for k in range (4):
                            coup2[k]=coup_enleve(grille2, coup2[k])
                            if k==0:
                                pieces3=[[],[],[],[]]
                                for m in range (len(pieces2[k])):
                                    if pieces2[k][m]!=j[0]:
                                        pieces3.append(pieces2[k][m])
                                coup2[k]=coup_rajoute(grille2, new_move(grille2, joueurs[k], j[2], j[3]), pieces3[k], joueurs[k])
                        Lgrille.append((grille2, pieces3, coup2))
        return coups_adversaires(Lgrille, pl, nb_pl_ia, 'B')
    else:
        #on récupère l'indice du joueur qu'on va simuler
        for p in range(3):
            if joueurs[p]==m:
                nb_pl=p+1
        for i in Lcoups: #lst[(grille, lst[pièces de tous les joueurs], lst[coups de tous les joueurs])] les deux derniers arguments sont une liste de 4 listes
            if i[2][nb_pl]!=[]: #si on a des coups possibles pour ce joueurs
                Lgrille=[]
                for j in (i[2][nb_pl]): #on récupère les coups de la forme (id_piece,color,pos_x,pos_y,rot,flip)
                    if j!=[]:
                        grille2=(placer_piece_grille20x20(i[0], j[0], j[2], j[3], j[1], j[4], j[5]))
                        coup2=i[2].copy() # on récupère les listes de tous les coups
                        pieces2=i[1].copy() #on récupères les listes de toutes les pièces
                        for k in range (4):
                            coup2[k]=coup_enleve(grille2, coup2[k])
                            if k==nb_pl:
                                pieces3=[[],[],[],[]]
                                for m in range (len(pieces2[k])):
                                    if pieces2[k][m]!=j[0]:
                                        pieces3[k].append(pieces2[k][m])
                                coup2[k]=coup_rajoute(grille2, new_move(grille2, joueurs[k], j[2], j[3]), pieces3[k], joueurs[k])
                        Lgrille.append((grille2, pieces3, coup2))
        return coups_adversaires(Lgrille, pl, nb_pl_ia, joueurs[nb_pl])

def coup_a_faire(pl, grille, n, id_game):
    '''
    fonction qui donne, par la méthode Monte Carlo, le coup à faire étant donné une grille de jeu et des pièces données
    :param pl: (str) G,Y,R,B = joueur
    :param grille: matrice 20*20
    :param n: (int) profondeur d'arbre à simuler / Compris entre 1 et 21
    :param id_game: id_game
    :return: le coup à faire de la forme (num_piece, x, y, rot, isFlipped)
    '''
    joueurs=['B', 'Y', 'R', 'G']
    pls_Plist=[]
    coups_poss_pl=[]
    #récupération listes des pièces restantes de chaque joueur + indice correspondant au joueur IA
    #récupération listes de coups possibles de chaque joueurs
    for i in range(len(joueurs)):
        pls_Plist.append(piece_res(id_game, joueurs[i]))
        coups_poss_pl.append(liste_coup_possible(id_game, joueurs[i]))
        if joueurs[i]==pl:
            pl_nb=i
    #création des arbres de coups possibles
    arbre=arbre_de_coups(pl, pl_nb, grille, pls_Plist, n, coups_poss_pl)
    
    #------analyse de l'arbre------
    
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