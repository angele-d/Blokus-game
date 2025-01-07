from pieces import *
from flask import g,Flask
import sqlite3
from placage_pieces import *
from logique_jeu import *


DATABASE = 'Base'
app = Flask(__name__)

# Crée une connexion avec la base ou récupère la connexion existante
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def malus(Pliste):
    '''
    Calcule le score (negatif) correspondant à une liste de pieces donnee
    :param Pliste: (tab) contient les id des pieces
    '''
    malus = 0
    for i in Pliste:
        print(i)
        for j in range(len(i)):
            for k in range(len(i)):
                if i[j][k]:
                    malus -= 1
    return malus

# Traduit une liste de nombre en pièce (matrice cf pieces.py)
def enleve(liste,restante):
    for i in range(len(liste)):
        if not i+1 in restante:
            liste = liste[:i] + liste[i+1:]
    return liste


def score(id_game):
    ''' 
    Calcule le score de chaque joueur dans un jeu donne
    :param Game: id_game de la base de données
    :return: Tableau [*,*,*,*] avec le score de chaque joueur [B,Y,R,G] de la partie Game
    :MaxIdcoup: [[id_coup,piece_correspondante_id_coup],..] 
                Utile uniquement pour verifier si P1 placee en dernier ou pas, selon joueur: [B,Y,R,G]
    '''
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM nom_joueur WHERE id_game = ?''',(id_game,))
    nbr= cursor.fetchone()[0]
    cursor.execute('''SELECT id_piece,color FROM coups WHERE id_game = ? GROUP BY color ORDER BY id_move DESC LIMIT 4''',(id_game,))
    derniere= cursor.fetchall()
    conn.close()
    Piece_restante_R = piece_restante(id_game,'B')
    Piece_restante_B = piece_restante(id_game,'Y')
    Piece_restante_Y = piece_restante(id_game,'R')
    if nbr != 3:
        Piece_restante_G = piece_restante(id_game,'G')
        # Dans l'ordre du dessus le score attribué à chaque couleur
        score =[0,0,0,0]
    else:
        score =[0,0,0]
    Tab_restante_R = enleve(Tabpiece.copy(),Piece_restante_R)
    Tab_restante_B = enleve(Tabpiece.copy(),Piece_restante_B)
    Tab_restante_Y = enleve(Tabpiece.copy(),Piece_restante_Y)
    if nbr != 3:
        Tab_restante_G = enleve(Tabpiece.copy(),Piece_restante_G)
    # Calcul des scores suivant le nombre de pièces qu'il reste pour chaque joueur       
    score[0] = malus(Tab_restante_B)
    score[1] = malus(Tab_restante_Y)
    score[2] = malus(Tab_restante_R) 
    if nbr != 3:
        score[3] = malus(Tab_restante_G)
    # Attribue les points bonus
    for i in range(len(score)):
        # Si le joueur a placé toutes ses pièces
        if score[i] == 0:
            score[i] = 15
            if nbr != 3:
                for i in derniere:
                    if i[0] == 'P1':
                        if i[1] == 'B':
                            score[0] = 20
                        if i[1] == 'Y':
                            score[1] = 20
                        if i[1] == 'R':
                            score[2] = 20
                        if i[1] == 'G':
                            score[3] = 20
            else :
                for i in derniere[:3]:
                    if i[0] == 'P1':
                        if i[1] == 'B':
                            score[0] = 20
                        if i[1] == 'Y':
                            score[1] = 20
                        if i[1] == 'R':
                            score[2] = 20
    # Si le joueur joue seul
    if nbr == 1:
        ind = 0
        for i in score:
            ind += i
        score = [ind]
    # S'il y avait deux joueurs dans la partie
    elif nbr == 2:
        ind = score[0]+score[2]
        ind2 = score[1]+score[3]
        score = [ind,ind2]
    conn.close()
    return score

if __name__ == "__main__":
    with app.app_context():
        print(score(135))

