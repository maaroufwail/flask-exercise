from flask import Blueprint, request, jsonify
from models import Artist
from extensions import db
from schemas import ArtistSchema

artist_bp = Blueprint('artist_bp', __name__, url_prefix='/api/artists')
artist_schema = ArtistSchema()
artist_list_schema = ArtistSchema(many=True)

@artist_bp.route('/', methods=['GET'])
def get_artists():
    artists = Artist.query.all()
    return jsonify(artist_list_schema.dump(artists)), 200

@artist_bp.route('/<int:id>', methods=['GET'])
def get_artist(id):
    artist = Artist.query.get_or_404(id)
    return jsonify(artist_schema.dump(artist)), 200

@artist_bp.route('/', methods=['POST'])
def create_artist():
    data = request.json
    new_artist = Artist(Name=data['Name'])
    db.session.add(new_artist)
    db.session.commit()
    return jsonify(artist_schema.dump(new_artist)), 201

@artist_bp.route('/<int:id>', methods=['PUT'])
def update_artist(id):
    artist = Artist.query.get_or_404(id)
    data = request.json
    artist.Name = data.get('Name', artist.Name)
    db.session.commit()
    return jsonify(artist_schema.dump(artist)), 200

@artist_bp.route('/<int:id>', methods=['DELETE'])
def delete_artist(id):
    artist = Artist.query.get_or_404(id)
    db.session.delete(artist)
    db.session.commit()
    return '', 204
