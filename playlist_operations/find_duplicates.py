from collections import defaultdict
from spotify_client import get_user_playlists, get_playlist_tracks

MENU_OPTION = '2'

def execute(sp):
    """Find duplicates across playlists"""
    user_playlists = get_user_playlists(sp)
    duplicates = find_duplicates_across_playlists(sp, user_playlists)
    if duplicates:
        print("\nDuplicate songs found across playlists (ordered by most duplicates):")
        for song, playlists in duplicates:
            print(f"\n{song} (appears in {len(playlists)} playlists)")
            for playlist in playlists:
                print(f"  - {playlist}")
    else:
        print("\nNo duplicate songs found across your playlists.")

def find_duplicates_across_playlists(sp, playlists):
    song_occurrences = defaultdict(list)
    
    for playlist in playlists:
        print(f"Fetching tracks from playlist: {playlist['name']}")
        tracks = get_playlist_tracks(sp, playlist['id'])
        for track in tracks:
            if track['track']:
                track_name = track['track']['name']
                artists = ", ".join([artist['name'] for artist in track['track']['artists']])
                song_key = f"{track_name} - {artists}"
                if playlist['name'] not in song_occurrences[song_key]:
                    song_occurrences[song_key].append(playlist['name'])
    
    duplicates = {song: playlists for song, playlists in song_occurrences.items() if len(playlists) > 1}
    sorted_duplicates = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_duplicates
