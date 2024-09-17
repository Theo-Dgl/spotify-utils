import os
import csv
from spotify_client import get_user_playlists, get_playlist_tracks

MENU_OPTION = '4'

def execute(sp):
    """Extract playlist info to CSV files"""
    user_playlists = get_user_playlists(sp)
    extract_playlist_info_to_csv(sp, user_playlists)

def extract_playlist_info_to_csv(sp, playlists):
    playlist_folder = 'playlists'
    os.makedirs(playlist_folder, exist_ok=True)

    for playlist in playlists:
        playlist_name = playlist['name']
        tracks = get_playlist_tracks(sp, playlist['id'])
        
        valid_filename = "".join([c for c in playlist_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = os.path.join(playlist_folder, f"{valid_filename.replace(' ', '_')}.csv")
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Track Name', 'Artist(s)', 'Album', 'Duration (ms)', 'Added At'])
            
            for track in tracks:
                if track['track']:
                    track_info = track['track']
                    track_name = track_info['name']
                    artists = ", ".join([artist['name'] for artist in track_info['artists']])
                    album = track_info['album']['name']
                    duration = track_info['duration_ms']
                    added_at = track['added_at']
                    csvwriter.writerow([track_name, artists, album, duration, added_at])
        
        print(f"Playlist '{playlist_name}' exported to {filename}")
