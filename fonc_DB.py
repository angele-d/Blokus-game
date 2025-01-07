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

def ajoute_coup(id_game,pl,x,y,m):
    '''
    Ajoute les coups possibles dans la BD
    :param id_game: id_game
    :param pl: joueur
    :param x: int
    :param y: int
    :param m: matrice 20x20
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    player = pl
    N_list = new_move(m,pl,x,y)
    Plist = piece_res(id_game,player)
    liste_coup = coup_rajoute_no_parral(m,N_list,Plist,pl)
    quest= '''INSERT INTO coups_possibles (id_game, id_piece, color, flip, rotation, position_x, position_y) 
               VALUES (?, ?, ?, ?, ?, ?, ?)'''
    cursor.executemany(quest, [
        (id_game, coup[0], coup[1], coup[5], coup[4], coup[2], coup[3]) 
        for coup in liste_coup
    ])
    conn.commit()
    conn.close()

def supprime_coups(m,x,y,id_game):
    '''
    Trouve et supprime les coups de la nouvelle matrice m  de la partie id_game ou on a joué un coup en x,y
    :param m: matrice de la partie où on a joué le nouveau coup
    :param x: position x du nouveau coup
    :param y: position y du nouveau coup
    :id_game: id de la game
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = '''
        SELECT id_piece, color, position_x, position_y, rotation, flip FROM coups_possibles WHERE id_game = ? '''
    cursor.execute(query, (id_game,))
    coup= cursor.fetchall()
    conn.close()
    a_del = coup_enleve_no_parral(m,coup)
    a_del = list(set(tuple(coup) for coup in a_del))
    supprime_coups_liste(id_game,a_del)

# Va chercher les coups possibles dans la BD
def cherche_coups_possibles(id_game):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''SELECT id_piece, color, position_x, position_y, rotation, flip FROM coups_possibles WHERE id_game = ?'''
    cursor.execute(query,(id_game,))
    coups_poss = cursor.fetchall()
    conn.close()
    return coups_poss


def supprime_coups_liste(id_game,liste):
    '''
    Supprime les coups dans liste
    :param id_game: int
    :param liste: elle contient [[id_piece, color, position_x, position_y, rotation, flip],...]
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''
    DELETE FROM coups_possibles
    WHERE id_game = :id_game AND (
        id_piece = :id_piece AND color = :color AND flip = :flip
        AND rotation = :rotation AND position_x = :position_x AND position_y = :position_y
    )'''
    formatted_data = [
        {
            'id_game': id_game,
            'id_piece': coup[0],
            'color': coup[1],
            'flip': coup[5],
            'rotation': coup[4],
            'position_x': coup[2],
            'position_y': coup[3]
        }
        for coup in liste
    ]
    cursor.executemany(query, formatted_data)
    conn.commit()
    conn.close()

def supprime_coups_piece(id_game,color,piece):
    '''
    Supprime tout les coups jouée avec la piece piece de la couleur color dans la partie id_game
    param:id_game: id de la partie
    param:color: couleur du joueur
    param:piece: piece à supprimer
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''DELETE FROM coups_possibles WHERE id_game = ? AND id_piece = ? AND color = ?'''
    cursor.execute(query,(id_game,piece,color))
    conn.commit()
    conn.close

def liste_coup_possible(id_game,color):
    ''' Donne la liste des coups possible pour le joueur color dans la partie id_game sous la forme:
    id_piece,color,pos_x,pos_y,rot,flip
    param:id_game: id de la partie
    param:color: couleur du joueur
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query= '''SELECT id_piece, color, position_x, position_y, rotation, flip FROM coups_possibles WHERE id_game = ? AND color = ?'''
    cursor.execute(query,(id_game,color))
    coups_poss = cursor.fetchall()
    conn.close()
    return coups_poss

def qui_peut_jouer(nb_joueur,id_game):
    '''
    Renvoie une liste des couleurs qui peuvent encore jouer
    :param nb_joueur: int
    :param id_game: int
    '''
    couleur = []
    l = liste_coup_possible(id_game,'B')
    if l != []:
        couleur += ['B']
    l = liste_coup_possible(id_game,'Y')
    if l != []:
        couleur += ['Y']
    l = liste_coup_possible(id_game,'R')
    if l != []:
        couleur += ['R']
    if nb_joueur != 3:
        l = liste_coup_possible(id_game,'G')
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
    qpj = qui_peut_jouer(nb_j,id_game)
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
        if not 'Y' in qpj:
            min_l[1]=100
        if not 'R' in qpj:
            min_l[2]=100
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

if __name__ == "__main__":
    with app.app_context():
        print(tour(135))