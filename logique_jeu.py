from pieces import *
from rotation_pieces import *

def print_jeu(m):
    '''
    Fonction auxiliaire faite pour le debugging
    '''
    for i in m:
        for j in i:
            print('[',j,']',end='')
        print('\n') 

def inside(i,j):
    '''renvoie le booléen suivant, check si le point(i,j) est dans la grille'''
    return (0 <= i < 20 and 0 <= j < 20)

def matrice_possible(m,pl):
    '''Fonction auxiliaire à coup possible, annote les case sur lequel la pièce doit passer et ne pas passer'''
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] == pl:
                if inside(i+1,j+1):
                    if m[i+1][j+1] == 'V':
                        m[i+1][j+1] = 'P'
                if inside(i-1,j+1):
                    if m[i-1][j+1] == 'V':
                        m[i-1][j+1] = 'P'
                if inside(i+1,j-1):
                    if m[i+1][j-1] == 'V':
                        m[i+1][j-1] = 'P'
                if inside(i-1,j-1):
                    if m[i-1][j-1] == 'V':
                        m[i-1][j-1] = 'P'
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] == pl:
                if inside(i+1,j):
                    if m[i+1][j] in ['V','P']:
                        m[i+1][j] = 'I'
                if inside(i-1,j):
                    if m[i-1][j] in ['V','P']:
                        m[i-1][j] = 'I'
                if inside(i,j+1):
                    if m[i][j+1] in ['V','P']:
                        m[i][j+1] = 'I'
                if inside(i,j-1):
                    if m[i][j-1] in ['V','P']:
                        m[i][j-1] = 'I'
    return m
                


def matrice_possible_start(pl):
    '''Renvoie une matrice avec l'emplacement de départ pour le joueur correspondant,
    à utiliser comme matrice pour les 4 premiers tours'''
    m = []
    for i in range(20):
        m.append([])
        for j in range(20):
            m[i].append(['V'])
    if pl == 'R':
        m[0][0] = 'P'
    if pl == 'Y':
        m[0][20] = 'P'
    if pl == 'B' :
        m[20][20] = 'P'
    if pl == 'G':
        m[20][0] = 'P'
    return m

def coup_restant_force_brute(m,pi,Plist):
    '''fonction EXTREMEMENT BOURRINE, pour calculer si il reste des coup possibles, a pas ou
    peu utiliser'''
    for i in range(2):
        if i == 1:
            isflipped = True
        else:
            isflipped = False
        for pl in Plist:
            for rot in range(1,5):
                for x in range(20):
                    for y in range(20):
                        if m[x][y] == 'V':
                            if coup_possible(m,pi,pl,x,y,rot,isflipped):
                                return True
    return False   

def coup_possible(m,pi,pl,x,y,rot,isflipped):
    '''Renvoie si le coup sur la matrice m de la pièce pi, par le joueur
    pl, aux coordonnées x,y de rotation rot et retourner suivant isflipped
    est'''
    if isflipped:
        pi = flip(pi)
    pi = rotation_piece_5x5(pi,rot)
    mat_pos = matrice_possible(m,pl)
    touche = False
    for i in range(len(pi)):
        for j in range (len(pi)):
            if pi[i][j]:
                if m[x+i-2][y+j-2] not in ['V','P']:
                    return False
                elif m[x+i-2][y+j-2] == 'P':
                    touche = True
    return touche
