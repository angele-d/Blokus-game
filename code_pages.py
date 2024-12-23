from flask import Flask, request, redirect, url_for, render_template, jsonify, session
from logique_jeu import *
from score import score
from placage_pieces import transcription_pieces_SQL_grille, generation_matrice_image
import sqlite3
import re

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

# Désigne le prochain joueur par sa couleur
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


def who_is_playing(id_move):
    color = id_move%4
    match color:
        case 0:
            return "B"
        case 1:
            return "Y"
        case 2:
            return "R"
        case 3:
            return "G"
        case _:
            print("Probleme sur color dans la BD")

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
    nb_move = -1 ### Si le nb_move passe a 0 ou plus, cela veut dire que la game est lancée
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
    #Ici, on doit choper toute les informations pour construire une page de lobby adaptée.
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
    #On modifie la base de donnée game, cela sera ensuite entendu par le script javascript qui redirigera
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
    #Ici, on écoute pour voir si on peut lancer la partie
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
#A SUPPRIMER PLUS TARD
def submit22():
    try:
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
        print(f"Coordonnées reçues: X={carrX}, Y={carrY}, Re={retourne}, Ro={rotation}, E={element},color={color},id_game={id_game}")
        flip = (retourne == -1)
        rotation = rotation//30
        numpiece= int(re.findall('\d+',element)[0])
        id_piece=f"P{numpiece}"
        id_move = 666 #GROS PLACEHOLDER LA TEAM IL FAUDRA METTRE EN PLACE LA LOGIQUE SUIVANTE POUR VOIR SI C'EST A SON TOUR
        player = color
        
        m = transcription_pieces_SQL_grille(id_game)
        if coup_possible(m,id_piece,color,int(carrX),int(carrY),int(rotation),flip):
             if color == player: #verif que c'est le bon joueur qui joue
                 insert_move(id_game, id_move, id_piece, color, int(carrX), int(carrY), int(rotation), flip)
                 # Retourne une réponse avec un statut et les coordonnées
                 return jsonify({"status": "coup valide"}), 200
             else: 
                 return jsonify({"status" : "pas le bon tour"}), 502
        else: 
             return jsonify({"status" : "coup_interdit"}), 501
    except Exception as e:
        # Gestion des erreurs et envoi d'une réponse appropriée
        print("erreur",e)
        return jsonify({"error": str(e)}), 500  # Erreur interne du serveur




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
    ##Il va falloir refaire la fonction....
    player = who_is_playing(id_move)
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

@app.route('/grille/<id_game>')
def grille(id_game):
    color = name_to_order(session['name'],id_game) #ATTENTION A NOTER : LES SESSIONS SONT RESET A CHAQUE LANCEMENT DU SERVEUR
    print("J'adore,la couleur",color)
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
    print("J'adore,la couleur",color)
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