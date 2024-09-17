import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8080/callback'
SCOPE = "playlist-read-private playlist-read-collaborative user-library-modify user-library-read playlist-modify-private playlist-modify-public  user-follow-modify"
CACHE_PATH = ".spotify_token_cache"
OPERATIONS_FOLDER = "playlist_operations"
