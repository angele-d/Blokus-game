import sqlite3
import re
from score import *

# Envoie le coup dans la base de données pour l'enregistrer
def insert_move(id_game, id_move, id_piece, color, position_x, position_y, rotation, flip):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO coups (id_game, id_move, id_piece, color, position_x, position_y, rotation, flip)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_game, id_move, id_piece, color, position_x, position_y, rotation, flip))
    conn.commit()
    conn.close()
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()

# Compte le nombre de joueur qu'il y a dans la partie
def nb_joueur(id_game):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM nom_joueur WHERE id_game = ?''',(id_game,))
    nb_joueur= cursor.fetchone()[0]
    conn.close()
    return nb_joueur

# Donne le nombre de pièces que le joueur à placer sur la grille
def nb_move(id_game,color):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''SELECT COUNT(*) FROM coups WHERE color = ? AND id_game = ?'''
    cursor.execute(query,(color,id_game))
    nb_move = cursor.fetchone()[0]
    conn.close()
    return nb_move

def ajoute_coup(id_game,x,y,m):
    '''
    Ajoute les coups possibles dans la BD
    :param id_game: id_game
    :param x: int
    :param y: int
    :param m: matrice 20x20
    '''
    cursor = conn.cursor()
    query= '''SELECT color FROM coups WHERE id_game = ? AND position_x = ? AND position_y = ?'''
    cursor.execute(query,(id_game,x,y))
    player = cursor.fetchone()[0]
    N_list = new_move(m,x,y)
    Plist = piece_restante(id_game,player)
    liste_coup = coup_rajoute(m,N_list,Plist)
    quest= '''INSERT INTO coups_possibles (id_game, id_piece, color, flip, rotation, position_x, position_y) 
               VALUES (?, ?, ?, ?, ?, ?, ?)'''
    for coup in liste_coup:
        cursor.execute(quest,(id_game,coup[0],coup[1],coup[5],coup[4],coup[2],coup[3]))
        conn.commit()
    conn.close()

# Va chercher les coups possibles dans la BD
def cherche_coups_possibles(id_game):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''SELECT id_piece, color, position_x, position_y, rotation, flip FROM coups_possibles WHERE id_game = ?'''
    cursor.execute(query,(id_game,))
    coups_poss = cursor.fetchall()
    conn.close()
    return coups_poss

def supprime_coups(m,x,y,id_game):
    '''
    Trouve et supprime les coups de la nouvelle matrice m  de la partie id_game ou on a joué un coup en x,y
    :param m: matrice de la partie où on a joué le nouveau coup
    :param x: 
    '''
    coup = coup_possible(id_game)
    a_check = []
    for i in coup:
        (id_piece,c,Px,Py,r,f) = i 
        if abs(px - x) <= 6:
            a_check.append(i)
    a_del = coup_enleve(m,a_check)
    supprime_coups_liste(id_game,a_del)


def supprime_coups_liste(id_game,liste):
    '''
    Supprime les coups dans liste
    :param id_game: int
    :param liste: elle contient [[id_piece, color, position_x, position_y, rotation, flip],...]
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''DELETE FROM coups_possibles WHERE id_game = ? AND id_piece = ? AND color = ? AND flip = ? AND rotation = ? AND position_x = ? AND position_y = ?'''
    for coup in liste:
        cursor.execute(query,(id_game,coup[0],coup[1],coup[5],coup[4],coup[2],coup[3]))
        conn.commit()
    conn.close()

def qui_peut_jouer(grille,nb_joueur,id_game):
    '''
    Renvoie une liste des couleurs qui peuvent encore jouer
    :param grille: matrice 20*20
    :param nb_joueur: int
    :param id_game: int
    '''
    Plist=piece_res(id_game,'B')
    couleur = []
    l = coups_possibles_force_brute(grille,'B',Plist)
    if l != []:
        couleur += ['B']
    Plist=piece_res(id_game,'Y')
    l = coups_possibles_force_brute(grille,'Y',Plist)
    if l != []:
        couleur += ['Y']
    if nb_joueur >= 3:
        Plist=piece_res(id_game,'R')
        l = coups_possibles_force_brute(grille,'R',Plist)
        if l != []:
            couleur += ['R']
    if nb_joueur >= 4:
        Plist=piece_res(id_game,'G')
        l = coups_possibles_force_brute(grille,'G',Plist)
        if l != []:
            couleur += ['G']
    return couleur

# Donne les pièces restantes d'un joueur sous forme ['P1','P2',...]
def piece_res(id_game,joueur):
    l = piece_restante(id_game,joueur)
    r = []
    for i in l:
        r += ['P'+str(i)]
    return r

# Renvoie la couleur du joueur à qui c'est le tour de jouer
def tour(id_game):
    m = transcription_pieces_SQL_grille(id_game)
    nb_j = nb_joueur(id_game)
    qpj = qui_peut_jouer(m,nb_j,id_game)
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''SELECT COUNT(*) FROM coups WHERE color = ? AND id_game = ?'''
    cursor.execute(query,("B",id_game))
    min_l = []
    coup_B = cursor.fetchone()[0]
    # Si plus personne ne peut jouer
    if qpj == []:
        conn.close()
        return m,None
    # Si personne n'a encore joué
    if coup_B == 0:
        conn.close()
        return m,"B"
    min_l.append(coup_B)

    cursor.execute(query,("Y",id_game))
    coup_Y= cursor.fetchone()[0]
    if coup_Y == 0:
        conn.close()
        return m,"Y"
    min_l.append(coup_Y)

    cursor.execute(query,("R",id_game))
    coup_R = cursor.fetchone()[0]
    if coup_R == 0:
        conn.close()
        return m,"R"
    min_l.append(coup_R)

    if nb_j != 3:
        cursor.execute(query,("G",id_game))
        coup_G = cursor.fetchone()[0]
        if coup_G == 0:
            conn.close()
            return m,"G"
        min_l.append(coup_G)
    conn.close()
    # Analyse qui peut encore jouer
    for i in range(4):
        if not 'B' in qpj:
            min_l[0]=100
        if nb_j >= 2:
            if not 'Y' in qpj:
                min_l[1]=100
        if nb_j >= 3:
            if not 'R' in qpj:
                min_l[2]=100
        if nb_j >= 4:
            if not 'G' in qpj:
                min_l[3]=100
    # Cherche la couleur à qui c'est le tour
    ind = min_l.index(min(min_l))
    if ind == 0:
        return m,"B"
    if ind == 1:
        return m,"Y"
    if ind == 2:
        return m,"R"
    return m,"G"
    

# Enregistre la partie dans la BD
def insert_game(id_game, name_game, password_game, nb_move):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO game (id_game, name_game, password_game, nb_move)
        VALUES (?, ?, ?, ?)
    ''', (id_game, name_game, password_game, nb_move))
    conn.commit()
    conn.close()

# Enregistre le nom des joueurs qui sont dans la partie id_game
def insert_name(id_game,name):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nom_joueur (id_game, nom)
        VALUES (?, ?)
    ''', (id_game, name))
    conn.commit()
    conn.close()

def name_to_order(name,id_game):
    '''
    Détermine la couleur du joueur "name" dans la partie id_game
    :param name: nom du joueur
    :param id_game: int
    :return: str
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nom FROM nom_joueur WHERE id_game = ? ''',(id_game,))
    rows = cursor.fetchall()
    conn.close()
    ind = -1
    for i in range(len(rows)):
        if rows[i][0] == name:
            ind = i
    if ind == 0:
        return 'B'
    elif ind == 1:
        return 'Y'
    elif ind == 2:
        return 'R'
    elif ind == 3:
        return 'G'  

# Cette fonction associe le nom du joueur à sa couleur
def order_to_name(couleur,id_game): 
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nom FROM nom_joueur WHERE id_game = ? ''',(id_game,))
    rows = cursor.fetchall()
    conn.close()
    nbr = len(rows)
    if nbr == 1:
        return rows[0][0]
    elif nbr == 2:
        if couleur == 'B':
            return rows[0][0]
        if couleur == 'Y':
            return rows[1][0]
        if couleur == 'R':
            return rows[0][0]
        if couleur == 'G':
            return rows[1][0]
    if couleur == 'B':
        return rows[0][0]
    if couleur == 'Y':
        return rows[1][0]
    if couleur == 'R':
        return rows[2][0]
    if couleur == 'G':
        return rows[3][0]

