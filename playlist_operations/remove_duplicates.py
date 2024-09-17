from spotify_client import get_user_playlists, get_playlist_tracks

MENU_OPTION = '1'

def execute(sp):
    """Remove duplicates within playlists"""
    user_playlists = get_user_playlists(sp)
    total_removed = 0
    for playlist in user_playlists:
        removed = remove_duplicates_from_playlist(sp, playlist['id'], playlist['name'])
        total_removed += removed
    print(f"\nTotal duplicates removed from all playlists: {total_removed}")

def remove_duplicates_from_playlist(sp, playlist_id, playlist_name):
    tracks = get_playlist_tracks(sp, playlist_id)
    unique_tracks = {}
    duplicates = []
    
    for i, item in enumerate(tracks):
        if item['track']:
            track = item['track']
            track_key = f"{track['name']} - {', '.join([artist['name'] for artist in track['artists']])}"
            if track_key not in unique_tracks:
                unique_tracks[track_key] = track['uri']
            else:
                duplicates.append((i, track_key))
    
    if duplicates:
        print(f"Removing {len(duplicates)} duplicate(s) from playlist: {playlist_name}")
        sp.playlist_remove_specific_occurrences_of_items(playlist_id, [{"uri": tracks[i]['track']['uri'], "positions": [i]} for i, _ in duplicates])
        return len(duplicates)
    else:
        print(f"No duplicates found in playlist: {playlist_name}")
        return 0
