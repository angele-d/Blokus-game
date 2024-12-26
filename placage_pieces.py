from pieces import P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21 #pieces.py
from rotation_pieces import transformation
from flask import g,Flask
from PIL import Image
import sqlite3

DATABASE = 'Base'
app = Flask(__name__)

def get_db(): # cette fonction permet de créer une connexion à la base 
              # ou de récupérer la connexion existante 
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#Manque les informations sur comment est faite la BD

def placer_piece_grille20x20(grille,num_piece,x,y,couleur,rotation,isflipped):
    '''
    Placage des pieces presentes dans la base de donnees, sur une grille 20x20
    PS: la verification de la validite des coups a deja ete faite
    :param grille: grille vide
    :param num_piece: (int) id_piece
    :param x: (int) position_x
    :param y: (int) position_y
    :param couleur: (string) R,B,Y ou G selon couleur du joueur
    :param rotation: (int) nombre de rotation a effectuer
    :param isflipped: (bool) true = piece retournee 
    :return: grille 20x20 avec pieces posees
    '''
    pi = globals()[num_piece]
    pi = transformation(pi,isflipped,rotation)
    for i in range(len(pi)):
        for j in range(len(pi[i])):
            if pi[i][j]:
                grille[x+i-2][y+j-2] = couleur # -2: car centre la piece est en (2,2) sur matrice 5x5
    return grille


def transcription_pieces_SQL_grille(Game):
    ''' 
    A PRIORI (car je n'ai aucun moyen de tester la fonction pour l'instant, n'ayant pas réellement la DB),
    renvoie la grille constituée des pièces deja mise dans la game d'ID_game valant game
    :param Game: id_game de table sql
    :return: matrice 20x20 des pieces placees dans la grille
    '''
    c = get_db().cursor()
    c.execute(f"SELECT id_Piece, position_x, position_y,color,rotation,flip FROM coups WHERE id_game = {Game}") # A CHANGER SI JAMAIS C'EST PLUS BON
    m = []
    for i in range(20):
        m.append([])
        for j in range(20):
            m[i].append('V')
    for tpl in c.fetchall():
        m = placer_piece_grille20x20(m,*tpl)
    return m

def generation_matrice_image(m,num_game):
    le = 3200
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
            tile_image=Image.open(path)
            result_image.paste(tile_image,(y,x))
    result_image.save(f"./static/grille{num_game}.png")