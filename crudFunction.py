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
        return {"success": False, "message": f"Errore durante l'inserimento: {str(e)}"}
    
    
def erase_artist(ArtistId):
    try:
        conn = get_db_connection()
        query = "DELETE FROM artists WHERE ArtistId = ?"
        conn.execute(query, (ArtistId,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Artista eliminato con successo."}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'eliminazione: {str(e)}"}

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
        return {"success": False, "message": f"Errore durante l'inserimento: {str(e)}"}

# funzione per eliminare un album avendo l'id dell'album
def erase_album(album_id):
    try:
        conn = get_db_connection()
        query = "DELETE FROM albums WHERE AlbumId = ?"
        conn.execute(query, (album_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Album eliminato con successo."}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'eliminazione: {str(e)}"}

