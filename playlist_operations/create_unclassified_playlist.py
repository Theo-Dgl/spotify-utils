from spotify_client import get_user_playlists, get_playlist_tracks, get_all_liked_songs

MENU_OPTION = '8'

def execute(sp):
    """Create 'Unclassified' playlist and add orphaned liked songs"""
    user_playlists = get_user_playlists(sp)
    playlist_url = create_unclassified_playlist_and_add_songs(sp, user_playlists)
    print(f"Unclassified playlist URL: {playlist_url}")

def create_unclassified_playlist_and_add_songs(sp, user_playlists):
    unclassified_playlist = next((playlist for playlist in user_playlists if playlist['name'].lower() == 'unclassified'), None)
    
    if not unclassified_playlist:
        user_id = sp.me()['id']
        unclassified_playlist = sp.user_playlist_create(user_id, 'Unclassified', public=False, description='Songs liked but not in any other playlist')
        print("Created 'Unclassified' playlist.")
    else:
        print("'Unclassified' playlist already exists.")

    liked_songs = get_all_liked_songs(sp)
    
    playlist_tracks = set()
    for playlist in user_playlists:
        if playlist['name'].lower() != 'unclassified':
            tracks = get_playlist_tracks(sp, playlist['id'])
            playlist_tracks.update(track['track']['id'] for track in tracks if track['track'])

    songs_to_add = []
    for song in liked_songs:
        if song['track']['id'] not in playlist_tracks:
            songs_to_add.append(song['track']['id'])

    if songs_to_add:
        for i in range(0, len(songs_to_add), 100):
            chunk = songs_to_add[i:i+100]
            sp.user_playlist_add_tracks(sp.me()['id'], unclassified_playlist['id'], chunk)
        
        print(f"Added {len(songs_to_add)} songs to 'Unclassified' playlist.")
    else:
        print("No songs to add to 'Unclassified' playlist.")

    return unclassified_playlist['external_urls']['spotify']