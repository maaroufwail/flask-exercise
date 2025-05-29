from flask import Flask, redirect, render_template, url_for, request
import sqlite3
import os

# Percorso del database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, './database/chinook.db')

# Funzione per ottenere la connessione al database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Per accedere ai risultati come dizionari
    return conn

# Funzione per inserire un artista viene usata pure per l'inserimento dell'album restituendo id del artista
# e gestice gli errori
def insert_artist(name):
    try:
        conn = get_db_connection()
        query = "INSERT INTO artists (name) VALUES (?)"
        conn.execute(query, (name,))
        id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.commit()
        conn.close()
        return {"success": True, "message": "Artista inserito con successo.", "data": id}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'inserimento dell'artista: {str(e)}"}
    
    
def erase_artist(ArtistId):
    try:
        conn = get_db_connection()
        # Prima elimina le tracce associate agli album dell'artista
        conn.execute("DELETE FROM tracks WHERE AlbumId IN (SELECT AlbumId FROM albums WHERE ArtistId = ?)", (ArtistId,))
        # Poi elimina gli album dell'artista
        conn.execute("DELETE FROM albums WHERE ArtistId = ?", (ArtistId,))
        # Infine elimina l'artista
        conn.execute("DELETE FROM artists WHERE ArtistId = ?", (ArtistId,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Artista eliminato con successo."}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'eliminazione dell'artista: {str(e)}"}

def get_artists():
    try:
        conn = get_db_connection()
        query = "SELECT * FROM artists"
        artists = conn.execute(query).fetchall()
        conn.close()
        return {"success": True, "data": artists}
    except Exception as e:
        return {"success": False, "message": f"Errore durante il recupero degli artisti: {str(e)}"}
    
# funzione per inserire un album ad un artista
def insert_album(title, ArtistId):
    try:
        conn = get_db_connection()
        query = "INSERT INTO albums (Title, ArtistId) VALUES (?, ?)"
        conn.execute(query, (title, ArtistId))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Album inserito con successo."}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'inserimento dell'album: {str(e)}"}

# funzione per eliminare un album avendo l'id dell'album e cancella anche le track che sono associate
def erase_album(album_id):
    try:
        conn = get_db_connection()
        query = "DELETE FROM tracks WHERE AlbumId = ?" 
        conn.execute(query, (album_id,))
        query = "DELETE FROM albums WHERE AlbumId = ?"
        conn.execute(query, (album_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Album eliminato con successo."}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'eliminazione dell'album: {str(e)}"}
    

def search_albums(title):
    try:
        conn = get_db_connection()
        query = "SELECT * FROM albums WHERE Title LIKE ?"
        albums = conn.execute(query, ('%' + title + '%',)).fetchall()
        conn.close()
        return {"success": True, "data": albums}
    except Exception as e:
        return {"success": False, "message": f"Errore durante la ricerca degli album: {str(e)}"}
    

#inserimento delle tracce di un album prendendo tutti i dati da un form 

def insert_track(track_name, album_id, media_type_id, genre_id, composer, milliseconds, bytes_val, unit_price):
    try:
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO Track 
            (Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (track_name, album_id, media_type_id, genre_id, composer, milliseconds, bytes_val, unit_price)
        )
        conn.commit()
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'inserimento della Track: {str(e)}"}

# funzione per ottenere i generi e media types per il form in modo che vedano solo le opzioni disponibili in un select
def form_track_get_data():
    try:
        conn = get_db_connection()
        media_types = conn.execute("SELECT MediaTypeId, Name FROM media_types").fetchall()
        genres = conn.execute("SELECT GenreId, Name FROM genres").fetchall()
        artists=get_artists().get("data")
        conn.close()

        return {"success": True, "media_types":media_types, "genres":genres, "artists":artists}
    except Exception as e:
        return {"success": False, "message": f"Errore durante il recupero dei generi e media types per il form delle track: {str(e)}"}

