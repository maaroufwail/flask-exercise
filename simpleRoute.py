
from flask import Flask, redirect, render_template, url_for, request
import sqlite3

import os

# Percorso del database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, './database/chinook.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Per accedere ai risultati come dizionari
    return conn


# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# la funzione route va a dirci a quali url va a rispondere la nostra applicazione
# visto che usiamo '/' come url, risponderà solo al caso univoco, usare una regex per 
# prendere più url
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'primo esempio di Flask!'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

#usiamo l'url per estrarre il dato che andiamo a mostrare
@app.route('/success/<user>/<age>')
def success(user, age):
    print(request.form["name"])
    return f"ti chiami { user } e hai { age } anni"

@app.route('/ricerca')
def try_login():
 return render_template('simpleForm.html')

@app.route('/artists')
def list_users():
    conn = get_db_connection()
    artists = conn.execute('SELECT * FROM artists').fetchall()
    conn.close()
    return render_template('artists.html', artists=artists)

# semplice ricerca di un artista 
@app.route('/ricerca-artista', methods=['POST', 'GET'])
def login():
    user = request.form["name"]
    conn= get_db_connection()
    query = "SELECT * FROM artists WHERE name LIKE ?"
    artists = conn.execute(query, (f"%{user}%",)).fetchall()
    print(artists)
    conn.close()

    return render_template("artists.html", artists=artists) 

#visualizzazione degli album di un artista 
@app.route('/album/<artist_id>')
def album(artist_id):
    conn = get_db_connection()
    query = "SELECT * FROM albums WHERE Artistid = ?"
    albums = conn.execute(query, (artist_id,)).fetchall()
    print(albums)
    conn.close()
    return render_template("albums.html", albums=albums)


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)