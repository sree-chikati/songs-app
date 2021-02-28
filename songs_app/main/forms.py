from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from songs_app.models import Song, Artist, Genre, Playlist, User

#Forms: 
# SongFrom, ArtistForm, GenreForm, PlaylistForm


class SongForm(FlaskForm):
    """Form to create a song."""
    title = StringField('Song Title',
        validators=[DataRequired(), Length(min=1, max=80)])
    photo_url = StringField('Photo', validators=[URL()])
    date = DateField('Date Released')
    artist = QuerySelectField('Artist',
        query_factory=lambda: Artist.query, allow_blank=False)
    genres = QuerySelectMultipleField('Genres',
        query_factory=lambda: Genre.query, allow_blank=False)
    playlists = QuerySelectMultipleField('Playlist',
        query_factory=lambda: Genre.query, allow_blank=False)
    submit = SubmitField('Submit')


class ArtistForm(FlaskForm):
    """Form to create an Artist."""
    name = StringField('Artist Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    about = TextAreaField('Information About Artist')
    submit = SubmitField('Submit')


class GenreForm(FlaskForm):
    """Form to create a genre."""
    name = StringField('Genre Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')


class PlaylistForm(FlaskForm):
    """Form to create a playlist."""
    name = StringField('Playlist Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')