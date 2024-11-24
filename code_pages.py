from flask import Flask, request, redirect, url_for, render_template
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
        insert_move(id_game, id_move, id_piece, color, position_x, position_y, rotation, flip)
        return "Move added successfully!", 200
    except Exception as e:
        return f"An error occured: {e}", 500

if __name__ == 'main':
    app.run(debug=True)