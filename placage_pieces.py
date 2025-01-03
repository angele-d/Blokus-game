from pieces import P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21 #pieces.py
from rotation_pieces import transformation
from flask import g,Flask
from PIL import Image
import sqlite3
import re

DATABASE = 'Base'
app = Flask(__name__)

# Permet de créer une connexion avec la base ou de récupérer la connexion existante 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def piece_restante(id_game,player):
    '''
    Donne les pièces qui restent à un joueur
    :param id_game: id_game dans la base SQL
    :param player: couleur du joueur dont on cherche les pièces restantes
    :return: liste de INT
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_piece FROM coups WHERE id_game = ? and color = ? ''',(id_game,player))
    rows = cursor.fetchall()
    conn.close()
    piece_jouee = []
    # Trouve toutes les pièces déjà jouées
    for i in range(len(rows)):
        piece = int(re.findall(r'P(\d+)', rows[i][0])[0])
        piece_jouee.append(piece)
    piece_res = []
    for i in range(1,22):
        if not i in piece_jouee:
            piece_res.append(i)
    return piece_res

def placer_piece_grille20x20(grille,num_piece,x,y,couleur,rotation,isflipped):
    '''
    Placage des pièces présentes dans la base de données sur une grille 20x20
    PS: la vérification de la validité des coups a déjà été faite
    :param grille: grille vide
    :param num_piece: (int) id_piece
    :param x: (int) position_x
    :param y: (int) position_y
    :param couleur: (string) R,B,Y ou G selon couleur du joueur
    :param rotation: (int) nombre de rotation à effectuer
    :param isflipped: (bool) true = pièce retournée 
    :return: grille 20x20 avec pièces posées
    '''
    pi = globals()[num_piece]
    pi = transformation(pi,isflipped,rotation)
    for i in range(len(pi)):
        for j in range(len(pi[i])):
            if pi[i][j]:
                # -2 car le centre la piece est en (2,2) sur matrice 5x5
                grille[x+i-2][y+j-2] = couleur
    return grille


def transcription_pieces_SQL_grille(Game):
    ''' 
    Renvoie la grille constituée des pièces déjà mise dans la game Game
    :param Game: id_game de table SQL
    :return: matrice 20x20 des pièces placées dans la grille
    '''
    c = get_db().cursor()
    c.execute(f"SELECT id_Piece, position_x, position_y,color,rotation,flip FROM coups WHERE id_game = {Game}")
    m = []
    for i in range(20):
        m.append([])
        for j in range(20):
            m[i].append('V')
    for tpl in c.fetchall():
        m = placer_piece_grille20x20(m,*tpl)
    return m

def generation_matrice_image(m,num_game):
    '''
    Génère la matrice présente dans grille.html
    :param m: matrice 20x20 des pieces placees dans la grille
    :param num_game: id_game de table sql
    :return: image de la nouvelle grille
    '''
    le = 3200
    if m[0][0] == 'V':
        m[0][0] = "SB"
    if m[0][19] =='V':
        m[0][19] = "SR"
    if m[19][19] == 'V':
        m[19][19] = "SY"
    if m[19][0] == 'V':
        m[19][0] = "SG"   
    result_image = Image.new("RGB", (le,le), (240,240,240))
    for i_index, i in enumerate(m):
        for j_index, tile in enumerate(i):
            x = 160 * i_index
            y = 160 * j_index
            if tile == 'R':
                path = './static/tiles/red.png'
            elif tile == 'G':
                path = './static/tiles/green.png'
            elif tile == 'Y':
                path = './static/tiles/yellow.png'
            elif tile == 'B':
                path = './static/tiles/blue.png'
            elif tile == 'V':
                path = './static/tiles/Empty.png'
            elif tile == "SB":
                path = './static/tiles/EmptyB.png'
            elif tile == "SR":
                path = './static/tiles/EmptyR.png'
            elif tile == "SG":
                path = './static/tiles/EmptyG.png'
            elif tile == "SY":
                path = './static/tiles/EmptyY.png'
            tile_image=Image.open(path)
            result_image.paste(tile_image,(y,x))
    result_image.save(f"./static/grille{num_game}.png")