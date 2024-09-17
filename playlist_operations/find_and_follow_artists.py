from collections import defaultdict
from spotify_client import get_user_playlists, get_playlist_tracks, get_all_liked_songs

MENU_OPTION = '9'

def execute(sp):
    """Follow artists with more than 3 liked songs"""
    artists_to_follow = find_and_follow_popular_artists(sp)
    if artists_to_follow:
        print("\nArtists followed based on your liked songs:")
        for artist, song_count in artists_to_follow:
            print(f"  - {artist} ({song_count} liked songs)")
    else:
        print("\nNo new artists to follow based on your liked songs.")

def find_and_follow_popular_artists(sp):
    print("Fetching your liked songs...")
    liked_songs = get_all_liked_songs(sp)
    
    artist_song_count = defaultdict(int)
    artist_ids = {}

    for song in liked_songs:
        for artist in song['track']['artists']:
            artist_name = artist['name']
            artist_song_count[artist_name] += 1
            artist_ids[artist_name] = artist['id']
    
    artists_to_follow = [(artist, count) for artist, count in artist_song_count.items() if count > 3]
    artists_to_follow.sort(key=lambda x: x[1], reverse=True)
    
    if artists_to_follow:
        print(f"Found {len(artists_to_follow)} artists with more than 3 liked songs.")
        artist_ids_to_follow = [artist_ids[artist] for artist, _ in artists_to_follow]
        
        # Follow artists in batches of 50 (Spotify API limit)
        for i in range(0, len(artist_ids_to_follow), 50):
            batch = artist_ids_to_follow[i:i+50]
            sp.user_follow_artists(batch)
        
        print(f"Successfully followed {len(artist_ids_to_follow)} artists.")
    else:
        print("No artists found with more than 3 liked songs.")

    return artists_to_follow