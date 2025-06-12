from flask import Blueprint, request, jsonify
from models import Genre
from extensions import db
from schemas import GenreSchema

genre_bp = Blueprint('genre_bp', __name__, url_prefix='/api/genres')
genre_schema = GenreSchema()
genre_list_schema = GenreSchema(many=True)

@genre_bp.route('/', methods=['GET'])
def get_genres():
    artists = Genre.query.all()
    return jsonify(genre_list_schema.dump(artists)), 200