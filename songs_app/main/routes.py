"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from songs_app.models import Song, Artist, Genre, Playlist, User
from songs_app.main.forms import SongForm, ArtistForm, GenreForm, PlaylistForm
from songs_app import bcrypt

# Import app and db from songs_app package so that we can run app
from songs_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def home():
    '''Display homepage'''
    all_users = User.query.all()
    return render_template('home.html', all_users=all_users)

@main.route('/user')
def user_page():
    all_playlists = Playlist.query.all()
    return render_template('user.html',
        all_playlists=all_playlists)


@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).one()
    current_playlists = user.playlists
    return render_template('profile.html',
        current_playlists=current_playlists)

@main.route('/playlists/<id>')
@login_required
def playlists(id):
    selected_playlist = Playlist.query.filter_by(id=id).one()
    all_songs = selected_playlist.songs
    return render_template('playlists.html',
    all_songs=all_songs)


@main.route('/create_song', methods=['GET', 'POST'])
@login_required
def create_song():
    form = SongForm()
    if form.validate_on_submit(): 
        new_song = Song(
            title=form.title.data,
            photo_url = form.photo_url.data,
            date=form.date.data,
            artist=form.artist.data,
            genres=form.genres.data,
            playlists=form.playlists.data
        )
        db.session.add(new_song)
        db.session.commit()

        flash('New song was created successfully.')
        return redirect(url_for('main.song_detail', song_id=new_song.id))
    return render_template('create_song.html', form=form)


@main.route('/create_artist', methods=['GET', 'POST'])
@login_required
def create_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data,
            about=form.about.data
        )
        db.session.add(new_artist)
        db.session.commit()

        flash('New artist created successfully.')
        return redirect(url_for('main.user_page'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_artist.html', form=form)


@main.route('/create_genre', methods=['GET', 'POST'])
@login_required
def create_genre():
    form = GenreForm()
    if form.validate_on_submit():
        new_genre = Genre(
            name=form.name.data
        )
        db.session.add(new_genre)
        db.session.commit()

        flash('New genre created successfully.')
        return redirect(url_for('main.user_page'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_genre.html', form=form)


@main.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        new_playlist = Playlist(
            name=form.name.data,
            user = current_user
        )
        db.session.add(new_playlist)
        db.session.commit()

        flash('New playlist created successfully.')
        return redirect(url_for('main.user_page'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_playlist.html', form=form)


@main.route('/song/<song_id>', methods=['GET', 'POST'])
@login_required
def song_detail(song_id):
    song = Song.query.filter_by(id=song_id).one()
    form = SongForm(obj=song)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        song.title = form.title.data
        song.photo_url = form.photo_url.data
        song.date = form.date.data
        song.artist = form.artist.data
        song.genres = form.genres.data
        song.playlists = form.playlists.data

        db.session.commit()

        flash('Song was updated successfully.')
        return redirect(url_for('main.song_detail', song_id=song_id))

    return render_template('song_detail.html', song=song, form=form)






    