from flask import Blueprint, request, jsonify
from models import Album, Track, Artist
from extensions import db
from schemas import AlbumSchema

album_bp = Blueprint('album_bp', __name__, url_prefix='/api/albums')
album_schema = AlbumSchema()
album_list_schema = AlbumSchema(many=True)

@album_bp.route('/', methods=['GET'])
def get_albums():
    # albums = Album.query.all()
    # return jsonify(album_list_schema.dump(albums)), 200

    actual_query = Album.query
    artist_id = request.args.get('artistId', type=int)
    genre_id = request.args.get('genreId', type=int)

    if artist_id:
        actual_query = actual_query.filter(Album.ArtistId == artist_id)
    if genre_id:
        # join con Track per filtrare album che contengono tracce di quel genere
        actual_query = actual_query.join(Track).filter(Track.GenreId == genre_id)

    # Opzionale: carica eager l'artista
    #query = query.options(joinedload(Album.artist))

    albums = actual_query.all()
    return jsonify(album_list_schema.dump(albums)), 200

@album_bp.route('/<int:id>', methods=['GET'])
def get_Album(id):
    album = Album.query.get_or_404(id)
    return jsonify(album_schema.dump(album)), 200



@album_bp.route('/', methods=['POST'])
def create_Album():
    json_data = request.get_json()
    # Validazione e deserializzazione
    new_album = album_schema.load(json_data)
    db.session.add(new_album)
    db.session.commit()
    return jsonify(album_schema.dump(new_album)), 201

@album_bp.route('/<int:id>', methods=['PUT'])
def update_Album(id):
    album = Album.query.get_or_404(id)
    data = request.json
    album.Title = data.get('Title', album.Title)
    db.session.commit()
    return jsonify(album_schema.dump(album)), 200

@album_bp.route('/<int:id>', methods=['DELETE'])
def delete_Album(id):
    album = Album.query.get_or_404(id)
    db.session.delete(album)
    db.session.commit()
    return '', 204