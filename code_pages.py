from flask import Flask, request, redirect, url_for, render_template, jsonify, session
from logique_jeu import *
from score import score,qui_peut_jouer
from placage_pieces import transcription_pieces_SQL_grille, generation_matrice_image
import sqlite3
import re
from deb_IA import *

app = Flask(__name__)
app.secret_key = "swV#]S)p;ArRak`*chzd3FC6BZG$j<95HU:/ga3{26mLf:r'eFHMSU5$!E]X&TAp=<kg;%Run`Q}CdvZS93gp6;eKjxH'$?}cFfuJ<D2`Nsh)(7_4~nXX-g2qb!7rGZ4BPAw]u6`/;a,=CmF3M.pVz#*_<DwtN3zuS;!J4F:.7Rqj?5Zgp}L)v^9G<y&AaB`d"

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
#NE FONCTIONNE PAS ENCORE
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
    if qpj == []:
        conn.close()
        return m,None
    if coup_B == None:
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
        if 'B' in qpj:
            min_l[0]=100
        elif 'Y' in qpj:
            min_l[1]=100
        elif 'R' in qpj:
            min_l[2]=100
        if 'G' in qpj:
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
    
##Piece restante donne les pièces qui restent a un joueur:
def piece_restante(id_game,player):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_piece FROM coups WHERE id_game = ? and color = ? ''',(id_game,player))
    rows = cursor.fetchall()
    conn.close()
    piece_jouee = []
    for i in range(len(rows)):
        piece = int(re.findall(r'P(\d+)', rows[i][0])[0])
        piece_jouee.append(piece)
    piece_restante = []
    for i in range(1,22):
        if not i in piece_jouee:
            piece_restante.append(i)
    return piece_restante


@app.route('/')
def accueil():
    return render_template('main_page.html')

@app.route('/join', methods=['GET','POST'])
def rejoin():
    if request.method == 'POST':
        mot_de_passe = request.form['password']
        nom_de_partie = request.form['game']
        nom_utilisateur = request.form['name']
        conn = sqlite3.connect('Base')
        cursor = conn.cursor()
        # Va chercher l'id de la partie pour orienter le joueur vers la bonne partie
        query = "SELECT id_game FROM game where password_game = ? and name_game = ?"
        cursor.execute(query,(mot_de_passe,nom_de_partie))
        rows = cursor.fetchall()
        # Pour chaque joueur est un nom différent dans une même partie
        quest = "SELECT COUNT(*) FROM nom_joueur JOIN game ON game.id_game = nom_joueur.id_game WHERE nom = ? AND name_game = ? AND nb_move = -1"
        cursor.execute(quest, (nom_utilisateur, nom_de_partie))
        count = cursor.fetchone()[0]
        conn.close()
        if count > 0:
            return "Ce nom est déjà pris"
        if len(rows) != 1:
            return "Mauvais mot de passe",500
        session[f'access_{rows[0][0]}'] = True
        ## LE NOM DE LA PERSONNE SERT PLUS TARD A CHOISIR L'ORDRE
        session['name'] = nom_utilisateur
        insert_name(rows[0][0],nom_utilisateur)
        return redirect(f"/game/{rows[0][0]}")
    return render_template('join_page.html')

@app.route('/newgame')
def new():
    return render_template('newgame.html')


@app.route('/newgame_db', methods=['POST'])
def newgame():
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "SELECT id_game FROM game ORDER BY id_game"
    cursor.execute(query)  
    rows = cursor.fetchall()  
    conn.close()
    i_a=0 
    found = False
    for i in range(1,len(rows)):
        if rows[i][0] != rows[i_a][0] + 1:
            newgame= rows[i_a] +1
            found = True
            break
        i_a += 1
    if not found:
        new_game = len(rows) + 1
    name = request.form['name']
    name_game = request.form['name_game']
    password_game = request.form['password_game']
    nb_move = -1 # Si le nb_move passe a 0 ou plus, cela veut dire que la game est lancée
    try:
        insert_name(new_game,name)
        insert_game(new_game,name_game,password_game,nb_move)
        session[f'access_{new_game}'] = True
        session[f'access_admin_{new_game}'] = True
        session['name'] = name
        return redirect(f"/game/{new_game}")
    except Exception as e:
        return f"L'erreur suivante à eu lieu: {e}", 500


@app.route('/getdatagame/<idgame>')
def getdatagame(idgame):
    # Récupère toutes les informations pour construire une page de lobby adaptée
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "SELECT nom from nom_joueur WHERE id_game = ?"
    cursor.execute(query,(idgame,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/addIA/<idgame>')
def addIA(idgame):
    #On compte le nombre d'IA qu'il y a dans la partie, puis on rajoute une IA si possible
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "SELECT COUNT(*) from nom_joueur WHERE id_game = ? AND nom GLOB 'IA[0-9]*'"
    cursor.execute(query,(idgame,))
    nb_IA = cursor.fetchone()[0]
    conn.close()
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "SELECT COUNT(*) from nom_joueur WHERE id_game = ?"
    cursor.execute(query,(idgame,))
    nb_joueur = cursor.fetchone()[0]
    conn.close()
    if nb_joueur < 4:
        insert_name(idgame,f"IA{nb_IA + 1}")
        return "IA ADDED",200
    return "TOO MUCH PLAYER", 200
 


@app.route('/launchgame/<idgame>',methods =['POST'])
def launchgame(idgame):
    #Modifie la base de donnée GAME, cela sera ensuite entendu par le script javascript qui redirigera
    #les joueurs
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "UPDATE game SET nb_move = 0 WHERE id_game = ?"
    cursor.execute(query,(idgame,))
    conn.commit()
    conn.close()
    return jsonify("Tout fonctionne")

@app.route('/getdatalaunch/<idgame>')
def getdatalaunch(idgame):
    #Ecoute pour voir si on peut lancer la partie
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "SELECT nb_move from game WHERE id_game = ?"
    cursor.execute(query,(idgame,))
    nb_move = cursor.fetchone()
    conn.close()
    if nb_move:
        return jsonify(nb_move[0])  
    else:
        return jsonify(-1)  


@app.route('/game/<idgame>')
def game(idgame):
    if not session.get(f'access_{idgame}'):
        return "Vous n'avez pas accès à la partie", 505
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "SELECT * FROM game WHERE id_game = ?"
    cursor.execute(query, (idgame,))  
    rows = cursor.fetchall()  
    conn.close()
    if rows == []:
        return "La partie n'existe pas",404
    else:
        if session.get(f'access_admin_{idgame}'):
            return render_template('lobby_admin.html',idgame=idgame)
        else:
            return render_template('lobby.html',idgame=idgame)



@app.route('/submit22', methods=['POST'])
def submit22():
    print("Requête reçue")
    #try:        
    # Récupère les données envoyées
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400  # Erreur si aucune donnée n'est reçue

    # Récupérer les coordonnées
    carrX = data.get('carrX')
    carrY = data.get('carrY')
    retourne = data.get('retourne')
    rotation = data.get('rotation')
    element = data.get('element')
    color = data.get('color')
    id_game= data.get('id_game')

    if carrX is None or carrY is None or retourne is None or rotation is None or element is None:
        return jsonify({"error": "Info manquante"}), 400  # Erreur si coordonnées manquantes

    # Traitements des données pour qu'ils soit transmis a la logique de jeu
    flip = (retourne == -1)
    rotation = rotation//30
    numpiece= int(re.findall('\d+',element)[0])
    id_piece=f"P{numpiece}"
    id_move = nb_move(id_game,color)
    
    m,player = tour(id_game)
    print("Info envoyée : Coord =",carrX,carrY,"pièce=",id_piece,"id_game =", id_game,"flip =", flip, "retourne=",retourne )
    
    if coup_possible(m,id_piece,color,int(carrY),int(carrX),int(rotation),flip):
        if color == player: #verif que c'est le bon joueur qui joue
            insert_move(id_game, id_move, id_piece, color, int(carrY), int(carrX), int(rotation), flip)
            # Retourne une réponse avec un statut et les coordonnées
            m,player = tour(id_game)
            if player == None:
                return jsonify({"status": "partie finie"}), 200
            return jsonify({"status": "coup valide"}), 200
        else: 
            print("Le joueur",color,"vaut jouer alors que c'est le tour de",player)
            return jsonify({"status" : "pas le bon tour"}), 200
    else: 
        return jsonify({"status" : "coup interdit"}), 200
    
    # except Exception as e:
    #     # Gestion des erreurs et envoi d'une réponse appropriée
    #     print("erreur:",e)
    #     return jsonify({"error": str(e)}), 500  # Erreur interne du serveur




#IL FAUT RENTRER LES CHOSES DE LA MANIERE SUIVANTE : ex : 5 	1 	P1 	R 	0 	0 	3 	0 (N'ECRIVEZ PAS FALSE)
@app.route('/submit', methods=['POST'])
def submit_form():
    id_game = request.form['id_game']
    id_move = request.form['id_move']
    id_piece = request.form['id_piece']
    color = request.form['color']
    position_x = request.form['position_x']
    position_y = request.form['position_y']
    rotation = request.form['rotation']
    flip = request.form['flip']
    player = who_is_playing(color)
    try:
        m = transcription_pieces_SQL_grille(id_game)
        if coup_possible(m,id_piece,color,int(position_x),int(position_y),int(rotation),bool(int(flip))):
            if color == player: #verif que c'est le bon joueur qui joue
                insert_move(id_game, id_move, id_piece, color, position_x, position_y, rotation, flip)
                return "Move added successfully!", 200
            else: 
                return "Le joueur n'est pas le bon", 500
        else: 
            return "Le coup n'est pas valide", 500
    except Exception as e:
        return f"An error occured: {e}", 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()  
    
    num_game = int(data.get('number')) 

    matrix = transcription_pieces_SQL_grille(num_game)
    
    generation_matrice_image(matrix,num_game)

    return jsonify({'image_url': f"/static/grille{num_game}.png"})

@app.route('/grille/<id_game>/fin_de_partie')
def fin_de_partie(id_game):
    sco = score(id_game)
    return render_template('fin_de_partie.html', score = sco)

@app.route('/grille/<id_game>')
def grille(id_game):
    if not session.get(f'access_{id_game}'):
        return "Vous n'avez pas accès à la partie", 505
    try :
        color = name_to_order(session['name'],id_game) #ATTENTION A NOTER : LES SESSIONS SONT RESET A CHAQUE LANCEMENT DU SERVEUR
    except Exception as e:
        print(f"pas de nom pour la partie :{id_game}")
        return f"pas de nom pour la partie :{id_game}",500
    liste_piece = piece_restante(id_game,color)
    coords = []
    for i in range(7):
        coords.append((1000,-10+130*i))
    for i in range(7):
        coords.append((1300,-10+130*i))
    for i in range(7):
        coords.append((1600,-10+130*i))
    for i in range(len(coords)):
        if not i+1 in liste_piece:
            coords[i] = None
    return render_template('grille.html',coords = coords, color = color,id_game = id_game)

#OUTIL DE DEBUG, A SUPPRIMER PLUS TARD
@app.route('/view_data')
def view_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('Base')
        cursor = conn.cursor()

        # Retrieve all rows from the "coups" table
        cursor.execute("SELECT * FROM coups")
        rows = cursor.fetchall()  # Fetch all rows as a list of tuples
        conn.close()

        # Pass the data to an HTML template
        return render_template('view_data.html', rows=rows)
    except Exception as e:
        return f"An error occurred while retrieving the data: {e}", 500

if __name__ == 'main':
    app.run(debug=True)