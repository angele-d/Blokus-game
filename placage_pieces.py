from pieces import P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21 #pieces.py
from rotation_pieces import transformation


import sqlite3
DATABASE = 'database.db' # Merci de mettre a jour cette ligne quand la database sera rajouté au 
#dépot github

def get_db(): # cette fonction permet de créer une connexion à la base 
              # ou de récupérer la connexion existante 
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#Manque les informations sur comment est faite la BD

def placer_piece_grille20x20(grille,num_piece,x,y,couleur,rotation,isflipped):
    pi = transformation(num_piece,isflipped,rotation)
    for i in range(len(pi)):
        for j in range(len(pi)):
            if pi[i][j]:
                grille[x+i-2][y+j-2] = couleur
    return grille


def transcription_pieces_SQL_grille(game):
    ''' A PRIORI (car je n'ai aucun moyen de tester la fonction pour l'instant, n'ayant pas réellement la DB),
    renvoie la grille constituée des pièces deja mise dans la game d'ID_game valant game'''
    c = get_db().cursor()
    c.execute(f"SELECT Id_Piece, Position_x, Position_y,Color,Rotation,Flip FROM COUPS WHERE Id_game = {Game}") # A CHANGER SI JAMAIS C'EST PLUS BON
    m = []
    for i in range(20):
        m.append([])
        for j in range(20):
            m[i].append(['V'])
    for tpl in c.fetchall():
        m = placer_piece_grille20x20(m,*tpl)
    return m

