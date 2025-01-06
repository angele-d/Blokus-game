from rotation_pieces import *
import time
import concurrent.futures
import os

def print_jeu(m):
    '''
    Fonction auxiliaire faite pour le debugging
    '''
    for i in m:
        for j in i:
            print('[',j,']',end='')
        print('\n') 

def inside(i,j):
    '''
    Vérifie que i et j correspondent bien aux coordonnées dans la grille 20x20
    :param i,j: (int)
    :return: (bool)
    '''
    return (0 <= i < 20 and 0 <= j < 20)

def matrice_possible(m,pl):
    '''
    Fonction auxiliaire à coup possible, annote les cases sur lequel la pièce suivante peut
    être posée (P) et ne peut pas être posée (I)
    :param m: matrice 20x20
    :param pl: (string) R,B,Y ou G = joueur
    :return: matrice 20x20 avec des P et I selon ou on peut poser la pièce suivante
    '''
    matrix = [[element for element in row] for row in m]
    vu = False
    for i in range(len(m)):
        for j in range(len(m)):
            if matrix[i][j] == pl: #correspond au bon joueur
                vu = True
                #verifie les coins: si vide -> mettre un P = on peut placer une piece
                if inside(i+1,j+1):
                    if matrix[i+1][j+1] == 'V':
                        matrix[i+1][j+1] = 'P'
                if inside(i-1,j+1):
                    if matrix[i-1][j+1] == 'V':
                        matrix[i-1][j+1] = 'P'
                if inside(i+1,j-1):
                    if matrix[i+1][j-1] == 'V':
                        matrix[i+1][j-1] = 'P'
                if inside(i-1,j-1):
                    if matrix[i-1][j-1] == 'V':
                        matrix[i-1][j-1] = 'P'
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] == pl: # Vérifie si cela correspond au bon joueur
                # Vérifie les contours: si vide ou P -> mettre un I = on peut pas placer une piece
                if inside(i+1,j):
                    if matrix[i+1][j] in ['V','P']:
                        matrix[i+1][j] = 'I'
                if inside(i-1,j):
                    if matrix[i-1][j] in ['V','P']:
                        matrix[i-1][j] = 'I'
                if inside(i,j+1):
                    if matrix[i][j+1] in ['V','P']:
                        matrix[i][j+1] = 'I'
                if inside(i,j-1):
                    if matrix[i][j-1] in ['V','P']:
                        matrix[i][j-1] = 'I'
    if not vu: #Si on est au tout debut / joueur a pas encore joue
        return(matrice_possible_start(pl))
    return matrix
                

def matrice_possible_start(pl):
    '''
    Renvoie une matrice avec l'emplacement de départ pour le joueur correspondant,
    à utiliser comme matrice pour les 4 premiers tours
    :param pl: (string) B,Y,R,G = joueur
    :return: matrice 20x20 avec P a l'endroit ou le joueur peut commencer a jouer
    '''
    m = []
    for i in range(20):
        m.append([])
        for j in range(20):
            m[i].append('V')
    if pl == 'B':
        m[0][0] = 'P'
    if pl == 'R':
        m[0][19] = 'P'
    if pl == 'Y' :
        m[19][19] = 'P'
    if pl == 'G':
        m[19][0] = 'P'
    return m

def new_move(m,pl,x,y):
    '''
    Fonction pour calculer les positions autour desquelles des nouveaux coups sont possibles
    :param m: matrice 20x20
    :param x: Position en x de la nouvelle pièce
    :param y: Position en y de la nouvelle pièce
    :return: (lst) liste des positions autour desquelles on peut faire des nouveaux coups
    '''
    deb =time.time()
    N_list =[]
    MP=matrice_possible(m, pl)
    for k in range(-3,4):
        for l in range(-3,4):
            new_x = x+k
            new_y = y+l
            if inside(new_x,new_y):
                if MP[new_x][new_y] == 'P':
                    N_list.append((new_x,new_y))
    fin = time.time()
    return N_list


def chunk_list(data, size):
    """
    Divise une liste en morceau de taille donnée
    """
    return [data[i:i + size] for i in range(0, len(data), size)]

def parall(chunk):
    """
    Fonction utilisée en parallèle pour déterminer si un coup est possible
    """
    results = []
    for params in chunk:
        if coup_possible(*params):
            (m,id_piece,c,c1,c2,c3,c4) = params
            results.append((id_piece,c,c1,c2,c3,c4))
    return results

def parallsupp(chunk):
    """Fonction utilisée en parallèle pour déterminer les coups non possibles
    """
    results = []
    for params in chunk:
        if not coup_possible(*params):
            (m,id_piece,c,c1,c2,c3,c4) = params
            results.append((id_piece,c,c1,c2,c3,c4))
    return results

def coup_rajoute(m,N_List,Plist,pl):
    '''
    Fonction pour calculer les nouveaux coups possibles aux positions N_List
    :param m: matrice 20x20
    :param N_list: Liste des nouvelles pos
    :Plist: liste des pièces du joueur
    :pl: joueur actuel
    :return: (lst) Liste des nouveaux coups
    '''
    start = time.time()
    to_check = []
    deb = time.time()
    MP=matrice_possible(m, pl)

    check_unique = set()
    for (new_x, new_y) in N_List:
        for i in range(2):
            if i == 1:
                isflipped = True
            else:
                isflipped = False
            for pi in Plist:
                for rot in range(1,5):
                    for k2 in range (-2,3):
                        for l2 in range (-2,3):
                            ajout_x= new_x+k2
                            ajout_y = new_y+l2
                            if inside(ajout_x,ajout_y) and (MP[ajout_x][ajout_y] in ['P','V']):
                                entry = (tuple(map(tuple, m)), pi, pl, ajout_x, ajout_y, rot, isflipped)
                                if not entry in check_unique:
                                    check_unique.add(entry)
                                    to_check.append((m,pi,pl,ajout_x,ajout_y,rot,isflipped))
    fin = time.time()
    coups = []

    chunk_size = max(1, len(to_check) // os.cpu_count())
    chunks = chunk_list(to_check, chunk_size)

    deb = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(parall, chunk) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                coups.extend(result)
    fin = time.time()

    return coups

def coup_rajoute_no_parral(m,N_list,Plist,pl):
    start = time.time()
    to_check = []
    deb = time.time()
    MP=matrice_possible(m, pl)

    check_unique = set()
    for (new_x, new_y) in N_list:
        for i in range(2):
            if i == 1:
                isflipped = True
            else:
                isflipped = False
            for pi in Plist:
                for rot in range(1,5):
                    for k2 in range (-2,3):
                        for l2 in range (-2,3):
                            ajout_x= new_x+k2
                            ajout_y = new_y+l2
                            if inside(ajout_x,ajout_y) and (MP[ajout_x][ajout_y] in ['P','V']):
                                entry = (tuple(map(tuple, m)), pi, pl, ajout_x, ajout_y, rot, isflipped)
                                if not entry in check_unique:
                                    check_unique.add(entry)
                                    to_check.append((MP,pi,pl,ajout_x,ajout_y,rot,isflipped))
    fin = time.time()
    coups = []
    for entry in to_check:
        if coup_possible_memo(*entry):
            (m,id_piece,c,c1,c2,c3,c4) = entry
            coups.append((id_piece,c,c1,c2,c3,c4))
    return coups


def coup_enleve(m,Clist):
    '''
    Fonction qui calcule quel coup ne sont plus possible
    :param m: Matrice de la partie
    :param Clist: Liste de coup
    :return: (lst) Liste des coups qui ne sont pas possible sur la matrice m
    '''
    if not Clist:
        return []
    Clist = [(m,pi,pl,x,y,rot,isflipped) for (pi,pl,x,y,rot,isflipped) in Clist ]
    chunk_size = max(1, len(Clist) // os.cpu_count())
    chunks = chunk_list(Clist, chunk_size)
    enleve =[]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(parallsupp, chunk) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                enleve.extend(result)
    return enleve

def coup_enleve_no_parral(m,Clist):
    '''
    Fonction qui calcule quel coup ne sont plus possible
    :param m: Matrice de la partie
    :param Clist: Liste de coup
    :return: (lst) Liste des coups qui ne sont pas possible sur la matrice m
    '''
    if not Clist:
        return []
    Clist = [(m,pi,pl,x,y,rot,isflipped) for (pi,pl,x,y,rot,isflipped) in Clist ]
    chunk_size = max(1, len(Clist) // os.cpu_count())
    chunks = chunk_list(Clist, chunk_size)
    enleve =[]
    for entry in enleve:
        if not coup_possible(*entry):
            (m,id_piece,c,c1,c2,c3,c4) = entry
            enleve.append((id_piece,c,c1,c2,c3,c4))
    return enleve



def coups_possibles_force_brute(m,pl,Plist):
    '''
    Fonction pour déterminer l'ensemble des coups possibles pour un joueur, moins brute
    :param m: matrice 20x20
    :param pl: (str) R,B,Y ou G = joueur
    :param Plist: liste de pieces
    :return: (lst) liste des coups possibles, sous la forme [(pi, x, y, rot, isflipped)]
    '''
    start = time.time()
    coups=[]
    MP=matrice_possible(m, pl)
    for i in range(2):
        if i == 1:
            isflipped = True
        else:
            isflipped = False
        for pi in Plist:
            for rot in range(1,5):
                for x in range(20):
                    for y in range(20):
                        if MP[x][y] == 'P':
                            for k in range(-2,3):
                                for l in range(-2,3):
                                    if inside(x+k,y+l) and (MP[x+k][y+l] in ['P','V']):
                                        if coup_possible(m,pi,pl,x,y,rot,isflipped): #Each should be on it's own thread
                                            coups.append((pi, x, y, rot, isflipped))
    end = time.time()
    return coups





def coup_possible(m,pi,pl,x,y,rot,isflipped):
    '''
    Renvoie si le coup sur la matrice m de la pièce pi, par le joueur
    pl, aux coordonnées x,y de rotation rot et retourne suivant isflipped
    est possible
    :param m: matrice 20x20
    :param pi: STRING DE LA VARIABLE DE LA matrice 5x5 de la piece
    :param pl: (str) R,B,Y ou G = joueur
    :param x,y: (int) coordonnees
    :param rot: (int) nombre de rotations
    :param isflipped: (bool) true = piece retournee
    :return: (bool) selon si coup possible ou pas
    '''
    pi = globals()[pi]
    pi = transformation(pi,isflipped,rot)
    mat_pos = matrice_possible(m,pl)
    touche = False
    for i in range(len(pi)):
        for j in range (len(pi)):
            if pi[i][j]:
                if x+i-2<0 or y+j-2<0:
                    #print("le coup a une coord négative")
                    return False
                if x+i-2>=20 or y+j-2>=20:
                    #print("le coup sort de la grille")
                    return False
                if mat_pos[x+i-2][y+j-2] not in ['V','P']:
                    return False
                elif mat_pos[x+i-2][y+j-2] == 'P':
                    touche = True
    return touche

def coup_possible_memo(mat_pos,pi,pl,x,y,rot,isflipped):
    pi = globals()[pi]
    pi = transformation(pi,isflipped,rot)
    touche = False
    for i in range(len(pi)):
        for j in range (len(pi)):
            if pi[i][j]:
                if x+i-2<0 or y+j-2<0:
                    #print("le coup a une coord négative")
                    return False
                if x+i-2>=20 or y+j-2>=20:
                    #print("le coup sort de la grille")
                    return False
                if mat_pos[x+i-2][y+j-2] not in ['V','P']:
                    return False
                elif mat_pos[x+i-2][y+j-2] == 'P':
                    touche = True
    return touche

def coup_restant_force_brute(grille, pl, Plist):
    '''
    :param grille: matrice 20x20
    :param pl: (str) G, Y, B, R = joueur
    :param Plist: Liste des pièces du joueur
    :return: (bool) il y a des coups possibles
    '''
    for i in range(2):
        if i == 1:
            isflipped = True
        else:
            isflipped = False
        MP=matrice_possible(grille, pl)
        for pi in Plist:
            for rot in range(1,5):
                for x in range(20):
                    for y in range(20):
                        if MP[x][y] == 'P':
                            if coup_possible(grille,pi,pl,x,y,rot,isflipped):
                                return True
    return False