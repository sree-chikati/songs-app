import os
from unittest import TestCase

from datetime import date
 
from songs_app import app, db, bcrypt
from songs_app.models import Song, Artist, Genre, Playlist, User

"""
Run these tests with the command:
python -m unittest songs_app.auth.tests
"""

#################################################
# Setup
#################################################

def create_songs():
    a1 = Artist(name='BTS')
    g1 = Genre(name= 'Pop')
    p1 = Playlist(name= 'Kpop')
    s1 = Song(
        title='Truth Untold',
        photo_url="https://c-sf.smule.com/rs-s89/arr/bd/e3/6f18462a-4308-433a-9b4b-321a617849cf_1024.jpg",
        date=date(2018, 8, 18),
        artist=a1,
        genres=g1,
        playlists=p1
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

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
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
    def test_signup(self):
        """Test signup route."""
        post_data = {
            'username': 'me-test@gmail.com',
            'name': 'me-test',
            'password': 'test123'
        }
        self.app.post('/signup', data = post_data)

        new_user = User.query.filter_by(username = 'me-test@gmail.com')
        self.assertIsNotNone(new_user)
    
    
    # TEST PASSED
    def test_signup_existing_user(self):
        """Test to see if user already exists."""
        post_data = {
            'username': 'test@gmail.com',
            'name': 'Test',
            'password': 'test'
        }
        self.app.post('/signup', data = post_data)

        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('That username is taken. Please choose a different one.', response_text)
    
    
    # TEST PASSED
    def test_login_correct_password(self):
        """Test with correct login passowrd."""
        create_user()

        post_data = {
            'username': 'test1',
            'name': 'Test1',
            'password': 'password'
        }
        self.app.post('/login', data = post_data)

        response = self.app.get('/', follow_redirects = True)
        response_text = response.get_data(as_text = True)

    
    # TEST PASSED
    def test_login_nonexistent_user(self):
        """Test with a non-existent user"""
        post_data = {
            'username': 'notreal',
            'name': 'Notreal',
            'password': 'notreal2'
        }
        response = self.app.post('/login', data = post_data)
       
        response_text = response.get_data(as_text=True)
        self.assertIn('No user with that username. Please try again.', response_text)
    
    
    # TEST PASSED
    def test_login_incorrect_password(self):
        """Test with incorrect password."""
        create_user()

        post_data = {
            'username': 'test1',
            'name': 'Test1',
            'password': 'wrong'
        }
        response = self.app.post('/login', data = post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn("Password doesn&#39;t match. Please try again.", response_text)
    
    
    # TEST PASSED
    def test_logout(self):
        """Test logout."""
        create_user()

        post_data = {
            'username': 'test1',
            'name': 'Test1',
            'password': 'password'
        }
        response = self.app.post('/login', data = post_data)
        response = self.app.get('/logout', follow_redirects = True)

        response_text = response.get_data(as_text=True)
        self.assertNotIn('You are logged in as me1', response_text)
