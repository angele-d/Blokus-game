from flask import Flask, request, redirect, url_for, render_template, jsonify, session
from flask_socketio import SocketIO, join_room, emit
from fonc_DB import *
from deb_IA import *
import sqlite3
import re
import time

app = Flask(__name__)
app.secret_key = "swV#]S)p;ArRak`*chzd3FC6BZG$j<95HU:/ga3{26mLf:r'eFHMSU5$!E]X&TAp=<kg;%Run`Q}CdvZS93gp6;eKjxH'$?}cFfuJ<D2`Nsh)(7_4~nXX-g2qb!7rGZ4BPAw]u6`/;a,=CmF3M.pVz#*_<DwtN3zuS;!J4F:.7Rqj?5Zgp}L)v^9G<y&AaB`d"

socketio = SocketIO(app)

@app.route('/')
def accueil():
    return render_template('main_page.html')

@app.route('/join', methods=['GET','POST'])
# Est appelé une première fois pour demander des informations qui serviront au deuxième appel pour rediriger vers le bon lobby
def join():
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
        if nom_utilisateur[:2] == "IA" or nom_utilisateur[-14:] == "(joueur local)":
            return "Choisissez un autre nom",500
        if count > 0:
            return "Ce nom est déjà pris",500
        if len(rows) != 1:
            return "Mauvais mot de passe",500
        # Pour donner les droits
        session[f'access_{rows[0][0]}'] = True
        session['name'] = nom_utilisateur
        insert_name(rows[0][0],nom_utilisateur)

        socketio.emit('join_room', {'room': rows[0][0]})

        return redirect(f"/game/{rows[0][0]}")
    return render_template('join_page.html')

@app.route('/rejoin', methods=['GET','POST'])
# Pour rejoindre une partie déjà lancée
def rejoin():
    if request.method == 'POST':
        mot_de_passe = request.form['password']
        nom_de_partie = request.form['game']
        nom_utilisateur = request.form['name']
        conn = sqlite3.connect('Base')
        cursor = conn.cursor()
        # Va chercher l'id de la partie pour orienter le joueur vers la bonne partie
        query = "SELECT id_game FROM game WHERE password_game = ? and name_game = ?"
        quest = "SELECT COUNT(*) FROM nom_joueur WHERE id_game = ? AND nom=?"
        cursor.execute(query,(mot_de_passe,nom_de_partie))
        rows = cursor.fetchall()
        if len(rows) != 1:
            conn.close()
            return "Mauvais mot de passe",500
        cursor.execute(quest,(rows[0][0],nom_utilisateur ))
        rowss = cursor.fetchall()
        conn.close()
        if len(rowss) == 0:
            return "Pas de joueur de ce nom dans cette partie"
        session[f'access_{rows[0][0]}'] = True
        # Pour rediriger directement vers le jeu et non vers le lobby
        session[f'access_admin_{rows[0][0]}'] = False
        session['name'] = nom_utilisateur
        socketio.emit('join_room', {'room': rows[0][0]})

        return redirect(f"/game/{rows[0][0]}")
    return render_template('rejoin_page.html')

@socketio.on('join_room')
def handle_join_room(data):
    print("un joueur a rejoint la room")
    room = data['room']
    join_room(room)
    emit('new_player', room=room)

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
            new_game= rows[i_a] +1
            found = True
            break
        i_a += 1
    if not found:
        new_game = len(rows) + 1
    name = request.form['name']
    name_game = request.form['name_game']
    password_game = request.form['password_game']
    nb_move = -1 # Si le nb_move passe a 0 ou plus, cela veut dire que la game est lancée
    if name[:2] == "IA" or name[-14:] == "(joueur local)":
            return "Choisissez un autre nom",500
    try:
        insert_name(new_game,name)
        insert_game(new_game,name_game,password_game,nb_move)
        session[f'access_{new_game}'] = True
        session[f'access_admin_{new_game}'] = True
        session['name'] = name

        socketio.emit('join_room', {'room': rows[0][0]})
        return redirect(f"/game/{new_game}")
    except Exception as e:
        return f"L'erreur suivante a eu lieu: {e}", 500

@app.route('/locale')
def locale():
    return render_template('locale.html')

@app.route('/locale_info', methods=['POST'])
def locale_info():
    nbr = request.form['nbr']
    return render_template('locale_info.html', nbr = int(nbr))

@app.route('/locale_lobby', methods=['POST'])
def locale_lobby():
    nbr_joue = []
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
            new_game= rows[i_a] +1
            found = True
            break
        i_a += 1
    if not found:
        new_game = len(rows) + 1
    for i in range(len(request.form)-2):
        name = request.form.get(f'name{i}')
        nbr_joue.append(name+"(joueur local)")
    name_game = request.form['name_game']
    password_game = request.form['password_game']
    nb_move = -1 # Si le nb_move passe a 0 ou plus, cela veut dire que la game est lancée
    try:
        for i in nbr_joue:
            insert_name(new_game,i)
        insert_game(new_game,name_game,password_game,nb_move)
        session[f'access_{new_game}'] = True
        session[f'access_admin_{new_game}'] = True
        session['name'] = nbr_joue[0]

        socketio.emit('join_room', {'room': rows[0][0]})
        return redirect(f"/game/{new_game}")
    except Exception as e:
        return f"L'erreur suivante a eu lieu: {e}", 500

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

@app.route('/addIA/<idgame>',methods=['POST'])
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
        print("addingIA")
        socketio.emit('new_player', room=idgame)
        print("IAadded")
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
    socketio.emit('launch', room = idgame)
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

def tourDeIA(id_game,playerColor):
    '''
    Verifie si le joueur qui a la main est une IA ou pas
    Effectue le coup de l'IA si c'est le cas
    Ne fait rien sinon
    :param id_game: (int)
    :param playerColor: (str) Y,B,R,G 
    '''
    playerName = order_to_name(playerColor,id_game)
    if re.match("IA\d",playerName) is not None: #c'est une IA
        print(f"{playerColor} est une IA")
        grille = transcription_pieces_SQL_grille(id_game)
        nextMove = coup_a_faire(playerColor,grille,3,id_game)
        num_piece, x, y, rot, isFlipped = nextMove
        if coup_possible(grille,num_piece,playerColor,x,y,rot,isFlipped):
            id_move = nb_move(id_game,playerColor)
            insert_move(id_game, id_move, num_piece, playerColor, x, y, rot, isFlipped)
            m = transcription_pieces_SQL_grille(id_game)
            ajoute_coup(id_game,playerColor,x,y,m)
            supprime_coups_piece(id_game,playerColor,num_piece)
            supprime_coups(m,x,y,id_game)
            socketio.emit('update_grille', room = id_game)
            next_player = tour(id_game)[1]
            if next_player == None:
                socketio.emit('fin_de_partie', room = id_game)
            socketio.emit('tour_joueur', room = id_game)
            return jsonify({"status": "coup valide","joueur":next_player}), 200 #next_player after the IA
    else:
        return jsonify({"status": "coup valide","joueur":playerColor}), 200 #This player because it's not an IA

@app.route('/submit22', methods=['POST'])
def submit22():
    print("Requête reçue")   
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
    numpiece= int(re.findall(r'\d+',element)[0])
    id_piece=f"P{numpiece}"
    id_move = nb_move(id_game,color)
    
    m,player = tour(id_game)
    print("Info envoyée : Coord =",carrX,carrY,"pièce=",id_piece,"id_game =", id_game,"flip =", flip, "rotation=",rotation )
    
    if coup_possible(m,id_piece,color,int(carrY),int(carrX),int(rotation),flip):
        if color == player: #verif que c'est le bon joueur qui joue
            insert_move(id_game, id_move, id_piece, color, int(carrY), int(carrX), int(rotation), flip)
            m = transcription_pieces_SQL_grille(id_game)
            ajoute_coup(id_game,color,int(carrY),int(carrX),m)
            print("DEBUG COUP_POSSIBLE",liste_coup_possible(id_game,"B"))
            supprime_coups_piece(id_game,color,id_piece)
            supprime_coups(m,int(carrY),int(carrX),id_game)
            socketio.emit('update_grille', room = id_game)
            # Retourne une réponse avec un statut et les coordonnées
            player = tour(id_game)[1]
            if player == None:
                socketio.emit('fin_de_partie', room = id_game)
            socketio.emit('tour_joueur', room = id_game)
            return tourDeIA(id_game,player)
        else: 
            print("Le joueur",color,"veut jouer alors que c'est le tour de",player)
            return jsonify({"status" : "pas le bon tour"}), 200
    else: 
        return jsonify({"status" : "coup interdit"}), 200
    
    # except Exception as e:
    #     # Gestion des erreurs et envoi d'une réponse appropriée
    #     print("erreur:",e)
    #     return jsonify({"error": str(e)}), 500  # Erreur interne du serveur


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()  
    
    num_game = int(data.get('number')) 

    matrix = transcription_pieces_SQL_grille(num_game)
    
    generation_matrice_image(matrix,num_game)

    return jsonify({'image_url': f"/static/grille{num_game}.png"})

@app.route('/joueur', methods=['POST'])
def joueur():
    data = request.get_json()
    id_game = int(data.get('number'))
    couleur = tour(id_game)[1]
    player = order_to_name(couleur,id_game)
    return jsonify({'joueur': player,"couleur":couleur})

@app.route('/fin_de_partie/<id_game>')
def fin_de_partie(id_game):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    query = "SELECT nom from nom_joueur WHERE id_game = ?"
    cursor.execute(query,(id_game,))
    d = cursor.fetchone()[0]
    conn.close()
    sco = score(id_game)
    return render_template('fin_de_partie.html', id_game = id_game, score = sco, liste_joueur = d)

@app.route('/grille/<id_game>')
def grille(id_game):
    print("tour",tour(159))

    if not session.get(f'access_{id_game}'):
        return "Vous n'avez pas accès à la partie", 505
    try :
        color = name_to_order(session['name'],id_game) #ATTENTION A NOTER : LES SESSIONS SONT RESET A CHAQUE LANCEMENT DU SERVEUR
    except Exception as e:
        print(f"pas de nom pour la partie :{id_game}")
        return f"pas de nom pour la partie :{id_game}",500
    nb_j = nb_joueur(id_game)
    m = transcription_pieces_SQL_grille(id_game)
    if cherche_coups_possibles(id_game) == []:
        ajoute_coup(id_game,"B",0,0,m)
        ajoute_coup(id_game,"Y",19,19,m)
        ajoute_coup(id_game,"R",0,19,m)
        ajoute_coup(id_game,"G",19,0,m)
    supprime_coups(m,0,0,id_game)

    if nb_j == 1 or session['name'][-14:] == "(joueur local)":
        (m,color) = tour(id_game)
        print("Joueur actuel:",color)
    if nb_j == 2:
        (m,j_actuel) = tour(id_game)
        if color == 'B':
            if j_actuel == 'Y' or j_actuel == 'R':
                color = 'R'
        else :
            if j_actuel == 'R' or j_actuel == 'G':
                color = 'G'            
            
    liste_piece = piece_restante(id_game,color)
    coords = []
    for i in range(7):
        coords.append((950,20+130*i))
    for i in range(7):
        coords.append((1150,20+130*i))
    for i in range(7):
        coords.append((1375,20+130*i))
    for i in range(len(coords)):
        if not i+1 in liste_piece:
            coords[i] = None
    return render_template('grille.html',coords = coords, color = color,id_game = id_game,nb_joueur = nb_j)


@app.route('/historique2')
def historique2():
    return render_template('historique2.html')

@app.route('/histo', methods=['GET','POST'])
def histo():
    if request.method == 'POST':
        mot_de_passe = request.form['password']
        nom_de_partie = request.form['game']
        conn = sqlite3.connect('Base')
        cursor = conn.cursor()
        # Pour trouver l'id de la partie
        quest = "SELECT id_game FROM game WHERE name_game = ? AND password_game = ?"
        cursor.execute(quest, (nom_de_partie, mot_de_passe))
        count = cursor.fetchone()
        conn.close()
        if count == None:
            id_game = 0
            return redirect(f"/historique/{id_game}/false")
    return redirect(f"/historique/{count[0]}/true")
    
@app.route('/historique/<id_game>/<boo>')
def historique(id_game,boo):
    try:
        if boo == "false":
            return redirect(f"/")
        conn = sqlite3.connect('Base')
        cursor = conn.cursor()
        # Retrouve tous les coups de la partie
        query = "SELECT * FROM coups WHERE id_game = ?"
        cursor.execute(query,(id_game,))
        coups = cursor.fetchall()
        conn.close()
        return render_template('historique.html', coups = coups)
    except Exception as e:
        return f"An error occurred while retrieving the data: {e}", 500


#FAIT AVEC DES PIECES JOUEES
if __name__ == '__main__':
    socketio.run(app, debug=True)
