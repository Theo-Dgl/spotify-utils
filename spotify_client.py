import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI, SCOPE, CACHE_PATH
import time

print(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI, SCOPE, CACHE_PATH)

def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=False,
        cache_path=CACHE_PATH
    )

    token_info = auth_manager.get_cached_token()

    if not token_info:
        auth_url = auth_manager.get_authorize_url()
        print(f"Please go to this URL and authorize the app: {auth_url}")
        response = input("Paste the full redirect URL here: ")
        code = auth_manager.parse_response_code(response)
        token_info = auth_manager.get_access_token(code)
    
    if is_token_expired(token_info):
        print("Token has expired, refreshing...")
        token_info = auth_manager.refresh_access_token(token_info['refresh_token'])
        auth_manager.cache_token(token_info)
    
    return spotipy.Spotify(auth=token_info['access_token'])

def is_token_expired(token_info):
    now = int(time.time())
    return token_info['expires_at'] - now < 60

def get_user_playlists(sp):
    playlists = []
    results = sp.current_user_playlists()
    user_id = sp.me()['id']
    while results:
        playlists.extend([playlist for playlist in results['items'] if playlist['owner']['id'] == user_id])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return playlists

def get_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        tracks.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return tracks

def get_all_liked_songs(sp):
    liked_songs = []
    results = sp.current_user_saved_tracks()
    while results:
        liked_songs.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return liked_songs

def get_current_user(sp):
    return sp.current_user()