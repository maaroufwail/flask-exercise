#scelte prese:
# - le variabili che vengono passate con il form usano il camelCase
# - le funzioni sono scritte in snake_case

from flask import Flask, jsonify, redirect, render_template, url_for, request
from flask_debugtoolbar import DebugToolbarExtension 
import sqlite3
from crudFunction import *
from extensions import db, ma
from flask_cors import CORS
from marshmallow import ValidationError

toolbar = DebugToolbarExtension()

def create_app(config_object='config.Config'):
    """
    Factory function per creare e configurare l'app Flask.
    - config_object: percorso alla classe di configurazione (es. 'config.Config')
    """

    app = Flask(__name__)
    app.config.from_object(config_object)

    # Abilito CORS (se il frontend Vue gira su un dominio/porta diversi)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Inizializzo le estensioni con l’app
    db.init_app(app)
    ma.init_app(app)

    # --------------------------------------------------------
    # 2. Gestione globale degli errori di validazione Marshmallow
    # --------------------------------------------------------
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        """
        Se Marshmallow solleva una ValidationError (es. nel schema.load())
        restituisco un JSON con i dettagli e codice 400.
        """
        return jsonify({"errors": err.messages}), 400

    # --------------------------------------------------------
    # 3. Importo e registro i Blueprint delle risorse
    #    (Assicurati di adattare i percorsi ai tuoi file)
    # --------------------------------------------------------
    from api.artistApi import artist_bp
    # from routes.albums import album_bp
    # from routes.tracks import track_bp
    # from routes.genres import genre_bp
    # from routes.media_types import media_type_bp

    app.register_blueprint(artist_bp,       url_prefix='/api/artists')
    # app.register_blueprint(album_bp,        url_prefix='/api/albums')
    # app.register_blueprint(track_bp,        url_prefix='/api/tracks')
    # app.register_blueprint(genre_bp,        url_prefix='/api/genres')
    # app.register_blueprint(media_type_bp,   url_prefix='/api/media_types')

    # --------------------------------------------------------
    # 4. Endpoint di “health check” (opzionale)
    # --------------------------------------------------------
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "OK", "message": "API in esecuzione"}), 200

    return app


# ------------------------------------------------------------
# 5. Punto di ingresso: creo e lancio l’app
# ------------------------------------------------------------
if __name__ == '__main__':
    # Se usi un file config.py, assicurati che la classe Config abbia almeno:
    #   SQLALCHEMY_DATABASE_URI, SECRET_KEY, JWT_SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS=False
    app = create_app()
    toolbar = DebugToolbarExtension(app)
    # Lascio debug=True in sviluppo, in produzione disabilitalo!
    app.run(host='127.0.0.1', port=5000, debug=True)