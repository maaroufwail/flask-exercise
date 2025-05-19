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

def insert_artist(name):
    try:
        conn = get_db_connection()
        query = "INSERT INTO artists (name) VALUES (?)"
        conn.execute(query, (name,))
        id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.commit()
        conn.close()
        return {"success": True, "message": "Artista inserito con successo."}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'inserimento: {str(e)}"}
    
    
def erase_artist(artist_id):
    try:
        conn = get_db_connection()
        query = "DELETE FROM artists WHERE ArtistId = ?"
        conn.execute(query, (artist_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Artista eliminato con successo."}
    except Exception as e:
        return {"success": False, "message": f"Errore durante l'eliminazione: {str(e)}"}

