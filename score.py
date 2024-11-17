from pieces import *

import sqlite3
DATABASE = 'database.db' # Merci de mettre a jour cette ligne quand la database sera rajouté au 
#dépot github

def get_db(): # cette fonction permet de créer une connexion à la base 
              # ou de récupérer la connexion existante 
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def score(Game):
    ''' Renvoie un tableau avec le score de chaque joueur de la partie Game'''
    c = get_db().cursor()
    query = "SELECT Id_Piece, Id_coup, Color FROM COUPS WHERE Id_game = ?"
    c.execute(query, (Game,))  
    P0=[]
    Piece_restante_R = piece_restante.copy()
    Piece_restante_B = piece_restante.copy()
    Piece_restante_Y = piece_restante.copy()
    Piece_restante_G = piece_restante.copy()
    Score =[0,0,0,0] #Dans l'ordre du dessus le score attribué a chaque couleur
    MaxIdcoup = [[0,P0],[0,P0],[0,P0],[0,P0]]
    for tpl in c.fetchall():
        if tpl[2] == 'R':
            MaxIdcoup[0][0] = max(MaxIdcoup[0],tpl[1])
            MaxIdcoup[0][1] = tpl[0]
            Piece_restante_R = [i for i in Piece_restante_R if i != tpl[0]]
        if tpl[2] == 'B':
            MaxIdcoup[1][0] = max(MaxIdcoup[1],tpl[1])
            MaxIdcoup[1][1] = tpl[0]
            Piece_restante_B = [i for i in Piece_restante_R if i != tpl[0]]
        if tpl[2] == 'Y':
            MaxIdcoup[0] = max(MaxIdcoup[2],tpl[1])
            MaxIdcoup[2][1] = tpl[0]
            Piece_restante_Y = [i for i in Piece_restante_R if i != tpl[0]]
        if tpl[2] == 'G':
            MaxIdcoup[0] = max(MaxIdcoup[3],tpl[1])
            MaxIdcoup[3][1] = tpl[0]
            Piece_restante_G = [i for i in Piece_restante_R if i != tpl[0]]
    score[0] = malus(Piece_restante_R)        
    score[1] = malus(Piece_restante_B)
    score[2] = malus(Piece_restante_Y)
    score[3] = malus(Piece_restante_G)
    for i in range(len(score)):
        if score[i] == 0:
            score[i] = 15
            if MaxIdcoup[1] == P1:
                score[i] = 20
    return score
    
def malus(Pliste):
    malus = 0
    for i in Plist:
        for j in range(len(i)):
            for k in range(len(i)):
                if i[j][k]:
                    malus = malus -1
    return malus

def piece_restante(joueur,game):
    reste = Tabpiece.copy()
