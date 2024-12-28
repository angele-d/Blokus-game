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

#Compte le nombre de joueur dans la partie
def nb_joueur(id_game):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM nom_joueur WHERE id_game = ?''',(id_game,))
    nb_joueur= cursor.fetchone()[0]
    conn.close()
    return nb_joueur

def nb_move(id_game,color):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''SELECT COUNT(*) FROM coups WHERE color = ? AND id_game = ?'''
    cursor.execute(query,("B",id_game))
    nb_move = cursor.fetchone()[0]
    conn.close()
    return nb_move

#Renvoie la couleur correspondante au joueur qui doit jouer
def qui_peut_jouer(grille,nb_joueur,id_game):
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

def piece_res(id_game,joueur):
    l = piece_restante(id_game,joueur)
    r = []
    for i in l:
        r += ['P'+str(i)]
    return r


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
    print(coup_B)
    if qpj == []:
        conn.close()
        return m,None
    if coup_B == 0:
        conn.close()
        return m,"B"
    min_l.append(coup_B)
    if nb_j >= 2:
        cursor.execute(query,("Y",id_game))
        coup_Y= cursor.fetchone()[0]
        if coup_Y == None:
            conn.close()
            return m,"Y"
        min_l.append(coup_Y)
    if nb_j >= 3:
        cursor.execute(query,("R",id_game))
        coup_R = cursor.fetchone()[0]
        if coup_R == None:
            conn.close()
            return m,"R"
        min_l.append(coup_R)
    if nb_j >= 4:
        cursor.execute(query,("G",id_game))
        coup_G = cursor.fetchone()[0]
        if coup_G == None:
            conn.close()
            return m,"G"
        min_l.append(coup_G)
    conn.close()
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
    ind = min_l.index(min(min_l))
    if ind == 0:
        return m,"B"
    if ind == 1:
        return m,"Y"
    if ind == 2:
        return m,"R"
    return m,"G"
    

# Enregistre la partie
def insert_game(id_game, name_game, password_game, nb_move):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO game (id_game, name_game, password_game, nb_move)
        VALUES (?, ?, ?, ?)
    ''', (id_game, name_game, password_game, nb_move))
    conn.commit()
    conn.close()

# Enregistre les joueurs qui sont dans la partie
def insert_name(id_game,name):
    #A RAJOUTER : PAS DEUX FOIS LE MEME NOM DANS LA MEME PARTIE, SINON PROBLEME DE CLEF PRIMAIRE
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nom_joueur (id_game, nom)
        VALUES (?, ?)
    ''', (id_game, name))
    conn.commit()
    conn.close()


#Détermine la couleur du joueur "name" dans la partie id_game
def name_to_order(name,id_game):
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
    print("Le joueur:",name,"a la couleur",ind)
    if ind == 0:
        return 'B'
    elif ind == 1:
        return 'Y'
    elif ind == 2:
        return 'R'
    elif ind == 3:
        return 'G'  
