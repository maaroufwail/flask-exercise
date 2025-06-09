from flask_sqlalchemy import SQLAlchemy
from extensions import db


class Artist(db.Model):
    __tablename__ = 'artists'
    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200))
    albums = db.relationship('Album', backref='artist', lazy=True)

class Album(db.Model):
    __tablename__ = 'albums'
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(160))
    ArtistId = db.Column(db.Integer, db.ForeignKey('artists.ArtistId'), nullable=False)
    tracks = db.relationship('Track', backref='album', lazy=True)

class Track(db.Model):
    __tablename__ = 'tracks'
    TrackId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200))
    AlbumId = db.Column(db.Integer, db.ForeignKey('albums.AlbumId'))
    MediaTypeId = db.Column(db.Integer, db.ForeignKey('media_types.MediaTypeId'))
    GenreId = db.Column(db.Integer, db.ForeignKey('genres.GenreId'))
    Composer = db.Column(db.String(220))
    Milliseconds = db.Column(db.Integer)
    Bytes = db.Column(db.Integer)
    UnitPrice = db.Column(db.Numeric)

class Genre(db.Model):
    __tablename__ = 'genres'
    GenreId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

class MediaType(db.Model):
    __tablename__ = 'media_types'
    MediaTypeId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

    
# E così via per Playlists, PlaylistTrack, Customers, Invoices, InvoiceItems, Employees
