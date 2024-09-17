from spotify_client import get_user_playlists, get_playlist_tracks

MENU_OPTION = '3'

def execute(sp):
    """Add all playlist tracks to Liked Songs"""
    user_playlists = get_user_playlists(sp)
    total_added = add_playlist_tracks_to_liked_songs(sp, user_playlists)
    print(f"\nTotal tracks added to Liked Songs: {total_added}")

def add_playlist_tracks_to_liked_songs(sp, playlists):
    all_track_ids = set()
    for playlist in playlists:
        print(f"Fetching tracks from playlist: {playlist['name']}")
        tracks = get_playlist_tracks(sp, playlist['id'])
        for track in tracks:
            if track['track'] and track['track']['id']:
                all_track_ids.add(track['track']['id'])
    
    print(f"Total unique tracks found: {len(all_track_ids)}")
    
    chunk_size = 50
    added_count = 0
    for i in range(0, len(all_track_ids), chunk_size):
        chunk = list(all_track_ids)[i:i+chunk_size]
        results = sp.current_user_saved_tracks_add(tracks=chunk)
        added_count += len(chunk)
        print(f"Added {added_count} tracks to Liked Songs")
    
    return added_count
