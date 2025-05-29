#scelte prese:
# - le variabili che vengono passate con il form usano il camelCase
# - le funzioni sono scritte in snake_case

from flask import Flask, jsonify, redirect, render_template, url_for, request
import sqlite3
from crudFunction import *

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





# route per la pagina di inserimento artista e titolo del album, il titotlo è opzionale
@app.route('/insert')
def insert():

    return render_template('insertArtistAlbum.html')


#route del effettivo inserimento dell'artista, nel caso in cui l'album non sia vuoto
# viene inserito anche l'album, altrimenti no
@app.route('/inserisci-artista-album', methods=['POST', 'GET'])
def inserisci_artista_album():
    if request.method != 'POST':
        return render_template('insertArtistAlbum.html')
    else:
        artist_name = request.form['artistName']
        album_title = request.form['albumTitle']
        idArtist=insert_artist(artist_name).get("data")
        if album_title:
            insert_album(album_title, idArtist)
        return redirect(url_for('list_users'))


#devo ancora implementare una cancellazione a cascata
@app.route('/delete-artist' , methods=['POST'])
def elimina_artista():
    ArtistId = request.form['ArtistId']
    erase_artist(ArtistId)
    return redirect(url_for('list_users'))


@app.route('/artists')
def list_users():
    artists= get_artists().get("data")
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
@app.route('/album/<ArtistId>')
def album(ArtistId):
    conn = get_db_connection()
    query = "SELECT * FROM albums WHERE Artistid = ?"
    albums = conn.execute(query, (ArtistId,)).fetchall()
    print(albums)
    conn.close()
    return render_template("albums.html", albums=albums)


#eliminiamo un album tramite l'id dell'album
@app.route('/delete-album' , methods=['POST'])
def elimina_album():
    album_id = request.form['AlbumId']
    print(album_id)
    erase_album(album_id)
    return redirect(url_for('list_users'))


#nel caso si arrivi al url senza POST darà per scontato che debbano ancora essere inseriti i dati
# altrimenti eseguirà l'inserimento dell'album e poi reindirizzerà alla lista degli artisti
@app.route('/album/<ArtistId>/insert-album', methods=['POST', 'GET'])
def inserisci_album(ArtistId):
    artist_id = ArtistId
    if request.method == 'POST':    
        album_title = request.form['albumTitle']
        insert_album(album_title, artist_id)
        return redirect(url_for('list_users'))
    else:
        print("non è un post")
        return render_template('insertAlbum.html' , ArtistId=artist_id)
    
# Zone per la gestione delle tracce
    
@app.route('/album/<AlbumId>/track')
def tracks( AlbumId):
    conn = get_db_connection()
    query = "SELECT * FROM tracks WHERE AlbumId = ?"
    tracks = conn.execute(query, (AlbumId,)).fetchall()
    print(tracks)
    conn.close()
    return render_template("tracks.html", tracks=tracks)

@app.route('/track/new', methods=['GET', 'POST'])
def new_track():
    if request.method == 'POST':
        # Recupera i dati inviati dal form
        track_name = request.form.get('name')
        # Per Album usiamo il campo nascosto che contiene l’ID selezionato dall’autocomplete
        album_id = request.form.get('album_id')
        media_type_id = request.form.get('media_type_id')
        genre_id = request.form.get('genre_id')
        composer = request.form.get('composer')
        milliseconds = request.form.get('milliseconds')
        bytes_val = request.form.get('bytes')
        unit_price = request.form.get('unit_price')
        insert_track(track_name, album_id, media_type_id, genre_id, composer, milliseconds, bytes_val, unit_price)
        return redirect(url_for('new_track'))

    # GET: recupera le opzioni per i select
    # Per l’autocomplete, la query per gli album viene effettuata tramite un’altra route
    form_data = form_track_get_data()
    if not form_data["success"]:
        return render_template("error.html", message=form_data["message"])
    media_types = form_data["media_types"]
    genres = form_data["genres"]

    return render_template("insertTrack.html",media_types=media_types, genres=genres)

@app.route('/search_albums')
def search_albums():
    # Questa route serve per restituire in JSON i suggerimenti per l’autocomplete degli album
    term = request.args.get('term', '')
    albums = search_albums(term)
    # Costruiamo l’elenco di suggerimenti nel formato compatibile con jQuery UI Autocomplete
    suggestions = [{'label': album['Title'], 'value': album['AlbumId']} for album in albums]
    return jsonify(suggestions)


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)