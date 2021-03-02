"""Initialize Config class to access environment variables."""
from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    """Set environment variables."""

    SQLALCHEMY_DATABASE_URI = os.getenv('postgres://clywduorbpvohe:f59934b277a0c99afb650791cede50c47f10eb2afe4c6ad2bb61448ec049c0e7@ec2-54-164-238-108.compute-1.amazonaws.com:5432/d5b7opmg078g79')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
