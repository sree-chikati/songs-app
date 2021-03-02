import os
import unittest

from datetime import date
 
from songs_app import app, db, bcrypt
from songs_app.models import Song, Artist, Genre, Playlist, User

"""
Run these tests with the command:
python -m unittest songs_app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_songs():
    a1 = Artist(name='BTS')
    s1 = Song(
        title='Truth Untold',
        photo_url="https://c-sf.smule.com/rs-s89/arr/bd/e3/6f18462a-4308-433a-9b4b-321a617849cf_1024.jpg",
        date=date(2018, 8, 18),
        artist=a1
    )
    db.session.add(s1)

    a2 = Artist(name='Shawn Mendes')
    s2 = Song(title='Wonder', artist=a2)
    db.session.add(s2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='test1', name='Test1', password=password_hash)
    db.session.add(user)
    db.session.commit()


#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    

    # TEST PASSED
    def test_create_song(self):
        """Test creating a song."""
        create_songs()
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'title':'Truth Untold',
            'photo_url':"https://c-sf.smule.com/rs-s89/arr/bd/e3/6f18462a-4308-433a-9b4b-321a617849cf_1024.jpg",
            'date': '2018-08-18',
            'artist':1
        }
        self.app.post('/create_song', data=post_data)

        created_song = Song.query.filter_by(title='Truth Untold')
        self.assertIsNotNone(created_song)
    
    
    # TEST PASSED
    def test_create_song_logged_out(self):
        """
        Test that the user is redirected when trying to access the create song 
        route if not logged in.
        """
        create_songs()
        create_user()

        response = self.app.get('/create_song')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_song', response.location)
    
    
    # TEST PASSED
    def test_create_artist(self):
        """Test creating an artist."""
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'name': 'BTS',
            'about': 'BTS, also known as the Bangtan Boys, is a seven-member South Korean boy band.'
        }
        self.app.post('/create_artist', data = post_data)

        new_artist = Artist.query.filter_by(name='BTS').one()
        self.assertIsNotNone(new_artist)
    

    # TEST PASSED
    def test_create_genre(self):
        """Test creating a genre."""
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'name': 'Pop'
        }
        self.app.post('/create_genre', data = post_data)

        new_genre = Genre.query.filter_by(name = 'Pop').one()
        self.assertIsNotNone(new_genre)
    
    
    # TEST PASSED
    def test_create_playlist(self):
        """Test creating a playlist."""
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'name': 'Pop Songs',
            'photo_url': 'https://f4.bcbits.com/img/a1630597668_10.jpg'
        }
        self.app.post('/create_playlist', data = post_data)

        new_playlist = Playlist.query.filter_by(name = 'Pop Songs').one()
        self.assertIsNotNone(new_playlist)
    
    
    # TEST PASSED
    def test_profile_page(self):
        """Test the profile page."""
        create_user()
        login(self.app, 'test1', 'password')
        db.session.commit()

        response = self.app.get('/profile/test1', follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('test1', response_text)