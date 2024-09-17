from tabulate import tabulate
from spotify_client import get_user_playlists, get_playlist_tracks, get_all_liked_songs

MENU_OPTION = '7'

def execute(sp):
    """Find liked songs not in playlists"""
    user_playlists = get_user_playlists(sp)
    find_liked_songs_not_in_playlists(sp, user_playlists)

def find_liked_songs_not_in_playlists(sp, playlists):
    liked_songs = get_all_liked_songs(sp)
    
    playlist_tracks = set()
    for playlist in playlists:
        tracks = get_playlist_tracks(sp, playlist['id'])
        playlist_tracks.update(track['track']['id'] for track in tracks if track['track'])

    songs_not_in_playlists = []
    for song in liked_songs:
        if song['track']['id'] not in playlist_tracks:
            songs_not_in_playlists.append(song['track'])

    table_data = []
    for song in songs_not_in_playlists:
        name = song['name']
        artists = ', '.join(artist['name'] for artist in song['artists'])
        link = song['external_urls']['spotify']
        table_data.append([name, artists, link])

    if table_data:
        print("\nLiked songs not in any playlist:")
        print(tabulate(table_data, headers=['Song', 'Artist(s)', 'Spotify Link'], tablefmt='grid'))
        print(f"\nTotal liked songs not in playlists: {len(songs_not_in_playlists)}")
    else:
        print("\nAll liked songs are in at least one playlist.")
