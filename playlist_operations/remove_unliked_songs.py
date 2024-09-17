from spotify_client import get_user_playlists, get_playlist_tracks

MENU_OPTION = '5'

def execute(sp):
    """Remove unliked songs from playlists"""
    user_playlists = get_user_playlists(sp)
    remove_unliked_songs(sp, user_playlists)

def remove_unliked_songs(sp, playlists):
    all_tracks = {}
    for playlist in playlists:
        tracks = get_playlist_tracks(sp, playlist['id'])
        for track in tracks:
            if track['track'] and track['track']['id']:
                track_id = track['track']['id']
                track_name = track['track']['name']
                artists = ", ".join([artist['name'] for artist in track['track']['artists']])
                if track_id not in all_tracks:
                    all_tracks[track_id] = {'name': track_name, 'artists': artists, 'playlists': []}
                all_tracks[track_id]['playlists'].append(playlist['name'])

    chunk_size = 50
    unliked_tracks = []
    for i in range(0, len(all_tracks), chunk_size):
        chunk = list(all_tracks.keys())[i:i+chunk_size]
        results = sp.current_user_saved_tracks_contains(tracks=chunk)
        for track_id, is_saved in zip(chunk, results):
            if not is_saved:
                unliked_tracks.append(track_id)

    if not unliked_tracks:
        print("No unliked songs found in your playlists.")
        return

    print("The following songs are not in your Liked Songs:")
    for i, track_id in enumerate(unliked_tracks, 1):
        track = all_tracks[track_id]
        print(f"{i}. {track['name']} - {track['artists']}")
        print(f"   Present in playlists: {', '.join(track['playlists'])}")

    choice = input("Do you want to remove these songs from all playlists? (y/n): ").lower()
    if choice == 'y':
        for playlist in playlists:
            tracks_to_remove = [track_id for track_id in unliked_tracks if playlist['name'] in all_tracks[track_id]['playlists']]
            if tracks_to_remove:
                sp.playlist_remove_all_occurrences_of_items(playlist['id'], tracks_to_remove)
                print(f"Removed {len(tracks_to_remove)} unliked tracks from '{playlist['name']}'")
        print("All unliked songs have been removed from your playlists.")
    else:
        print("No changes were made to your playlists.")
