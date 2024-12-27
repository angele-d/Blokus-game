from pieces import *
from flask import g,Flask
import sqlite3
from deb_IA import *
from code_pages import *

DATABASE = 'BaseTest' # Merci de mettre a jour cette ligne quand la database sera rajouté au dépot github
app = Flask(__name__)

def qui_peut_jouer(grille,nb_joueur,id_game):
    Plist=piece_restante(id_game,'B')
    couleur = []
    l = coups_possibles_force_brute(grille,'B',Plist)
    if l == []:
        couleur =+ ['B']
    Plist=piece_restante(id_game,'Y')
    l = coups_possibles_force_brute(grille,'Y',Plist)
    if l == []:
        couleur =+ ['Y']
    if nb_joueur >= 3:
        Plist=piece_restante(id_game,'R')
        l = coups_possibles_force_brute(grille,'R',Plist)
        if l == []:
            couleur =+ ['R']
    if nb_joueur >= 4:
        Plist=piece_restante(id_game,'G')
        l = coups_possibles_force_brute(grille,'G',Plist)
        if l == []:
            couleur =+ ['G']
    return couleur

def get_db(): # cette fonction permet de créer une connexion à la base 
              # ou de récupérer la connexion existante 
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def malus(Pliste):
    '''
    Calcule le score (negatif) correspondant a une liste de pieces donnee
    :param Pliste: (tab) contient les id des pieces
    '''
    malus = 0
    for i in Pliste:
        for j in range(len(i)):
            for k in range(len(i)):
                if i[j][k]:
                    malus = malus -1
    return malus



def score(Game): #IL EST POSSIBLE QU'IL FASSE CHANGER CE CODE, CE QUI EST ICI N'A PAS L'AIR HYPER SEIN
    # ON FERME JAMAIS LA CONNECTION PAR EXEMPLE...
    ''' 
    Calcule le score de chaque joueur dans un jeu donne
    :param Game: id_game de la base de données
    :return: Tableau [*,*,*,*] avec le score de chaque joueur [R,B,Y,G] de la partie Game
    :MaxIdcoup: [[id_coup,piece_correspondante_id_coup],..] 
                Utile uniquement pour verifier si P1 placee en dernier ou pas, selon joueur: [R,B,Y,G]
    '''
    c = get_db().cursor()
    query = "SELECT id_piece, id_move, color FROM coups WHERE id_game = ?"
    c.execute(query, (Game,))  
    P0=[]
    Piece_restante_R = Tabpiece.copy()
    Piece_restante_B = Tabpiece.copy()
    Piece_restante_Y = Tabpiece.copy()
    Piece_restante_G = Tabpiece.copy()
    score =[0,0,0,0] #Dans l'ordre du dessus le score attribué a chaque couleur
    MaxIdcoup = [[0,P0],[0,P0],[0,P0],[0,P0]] #Valeurs de base, qui n'arrivent jamais
    for tpl in c.fetchall(): #chaque tuple de la requete
        if tpl[2] == 'R':
            if MaxIdcoup[0][0] < tpl[1]: #verifie qu'on a toujours le dernier coup de R dans MaxIdcoup
                MaxIdcoup[0][0] = tpl[1]
                MaxIdcoup[0][1] = tpl[0]
            Piece_restante_R = [i for i in Piece_restante_R if i != tpl[0]] #Garde pieces =/ coup etudie
        if tpl[2] == 'B':
            if MaxIdcoup[1][0] < tpl[1]: #verifie qu'on a toujours le dernier coup de B dans MaxIdcoup
                MaxIdcoup[1][0] = tpl[1]
                MaxIdcoup[1][1] = tpl[0]
            Piece_restante_B = [i for i in Piece_restante_B if i != tpl[0]] #Garde pieces =/ coup etudie
        if tpl[2] == 'Y':
            if MaxIdcoup[2][0] < tpl[1]: #verifie qu'on a toujours le dernier coup de Y dans MaxIdcoup
                MaxIdcoup[2][0] = tpl[1]
                MaxIdcoup[2][1] = tpl[0]
            Piece_restante_Y = [i for i in Piece_restante_Y if i != tpl[0]] #Garde pieces =/ coup etudie
        if tpl[2] == 'G':
            if MaxIdcoup[3][0] < tpl[1]: #verifie qu'on a toujours le dernier coup de G dans MaxIdcoup
                MaxIdcoup[3][0] = tpl[1]
                MaxIdcoup[3][1] = tpl[0]
            Piece_restante_G = [i for i in Piece_restante_G if i != tpl[0]] #Garde pieces =/ coup etudie
    #Calcul des scores suivant le nombre de pieces qu'il reste pour chaque joueur
    score[0] = malus(Piece_restante_R)        
    score[1] = malus(Piece_restante_B)
    score[2] = malus(Piece_restante_Y)
    score[3] = malus(Piece_restante_G)
    for i in range(len(score)): #Points bonus
        if score[i] == 0: #Cad que le joueur a place toutes ses pieces
            score[i] = 15
            if MaxIdcoup[1] == P1: #Cad que le dernier coup joue est le carre solitaire
                score[i] = 20
    return score

if __name__ == "__main__":
    with app.app_context():
        print(score(1))

