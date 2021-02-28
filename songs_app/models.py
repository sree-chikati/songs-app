"""Create database models to represent tables."""
from songs_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

# Models & Tables: 
# Playlist, Song, playlist_songs_table
# Artist, Genre, songs_genre_table
# User, user_playlist_table

class Song(db.Model):
    """Song model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(URLType)
    date = db.Column(db.Date)

    # The Artist who composed the song
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', back_populates='songs')

    # The genres of a song can be
    genres = db.relationship(
        'Genre', secondary='song_genre', back_populates='songs')
    
    # What playlist does this song belong to?
    playlists = db.relationship(
        'Playlist', secondary='song_in_playlist', back_populates='songs')


class Artist(db.Model):
    """Artist model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(250))
    
    # The Songs composed by the Artist
    songs = db.relationship('Song', back_populates='artist')
    

class Genre(db.Model):
    """Genre model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # The genre a song belongs to
    songs = db.relationship(
        'Song', secondary='song_genre', back_populates='genres')

songs_genre_table = db.Table('song_genre',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)


class Playlist(db.Model):
    """Playlist model."""
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(URLType)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Which song is in this playlist?
    songs = db.relationship(
        'Song', secondary='song_in_playlist', back_populates='playlists')

    # The user who owns the playlist
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='playlists')


playlist_songs_table = db.Table('song_in_playlist',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
)


class User(UserMixin, db.Model):
    """Playlist model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    # The playlists part of User
    playlists = db.relationship('Playlist', back_populates='user')
