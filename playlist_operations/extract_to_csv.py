import os
import csv
from spotify_client import get_user_playlists, get_playlist_tracks, get_current_user

MENU_OPTION = '4'

def execute(sp):
    """Extract playlist info to CSV files"""
    user = get_current_user(sp)
    user_name = user['display_name']
    user_playlists = get_user_playlists(sp)
    extract_playlist_info_to_csv(sp, user_playlists, user_name)

def extract_playlist_info_to_csv(sp, playlists, user_name):
    base_folder = 'playlists'
    user_folder = os.path.join(base_folder, user_name)
    os.makedirs(user_folder, exist_ok=True)

    for playlist in playlists:
        playlist_name = playlist['name']
        tracks = get_playlist_tracks(sp, playlist['id'])
        
        valid_filename = "".join([c for c in playlist_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = os.path.join(user_folder, f"{valid_filename.replace(' ', '_')}.csv")
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Track Name', 'Artist(s)', 'Album', 'Duration (ms)', 'Added At', 'Spotify ID', 'Spotify URL'])
            
            for track in tracks:
                if track['track']:
                    track_info = track['track']
                    track_name = track_info['name']
                    artists = ", ".join([artist['name'] for artist in track_info['artists']])
                    album = track_info['album']['name']
                    duration = track_info['duration_ms']
                    added_at = track['added_at']
                    spotify_id = track_info['id']
                    spotify_url = track_info['external_urls']['spotify']
                    csvwriter.writerow([track_name, artists, album, duration, added_at, spotify_id, spotify_url])
        
        print(f"Playlist '{playlist_name}' exported to {filename}")
