from flask import Flask, request, redirect, url_for, render_template
from logique_jeu import *
from score import score
from placage_pieces import transcription_pieces_SQL_grille
import sqlite3


app = Flask(__name__)

def insert_move(id_game, id_move, id_piece, color, position_x, position_y, rotation, flip):
    conn = sqlite3.connect('Base')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO coups (id_game, id_move, id_piece, color, position_x, position_y, rotation, flip)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_game, id_move, id_piece, color, position_x, position_y, rotation, flip))
    conn.commit()
    conn.close()

@app.route('/')
def accueil():
    return render_template('home_page.html')

@app.route('/game')
def game():
    return render_template('game_page.html')

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
    try:
        m = transcription_pieces_SQL_grille(id_game)
        if coup_possible(m,id_piece,color,int(position_x),int(position_y),int(rotation),bool(int(flip))):
            insert_move(id_game, id_move, id_piece, color, position_x, position_y, rotation, flip)
            return "Move added successfully!", 200
        else: 
            return "Le coup n'est pas valide", 500
    except Exception as e:
        return f"An error occured: {e}", 500

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