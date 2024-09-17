from collections import defaultdict
from spotify_client import get_user_playlists, get_playlist_tracks

MENU_OPTION = '6'

def execute(sp):
    """Analyze similarity across all playlists"""
    user_playlists = get_user_playlists(sp)
    analyze_all_playlist_similarities(sp, user_playlists)

def analyze_all_playlist_similarities(sp, playlists):
    if len(playlists) < 2:
        print("You need at least two playlists to compare.")
        return

    playlist_tracks = {}
    for playlist in playlists:
        tracks = get_playlist_tracks(sp, playlist['id'])
        playlist_tracks[playlist['id']] = set(track['track']['id'] for track in tracks if track['track'])

    similarities = []
    for i, playlist1 in enumerate(playlists):
        for j, playlist2 in enumerate(playlists[i+1:], i+1):
            common_tracks = playlist_tracks[playlist1['id']].intersection(playlist_tracks[playlist2['id']])
            if common_tracks:  # Only process if there are common tracks
                similarity_percentage = (len(common_tracks) / max(len(playlist_tracks[playlist1['id']]), len(playlist_tracks[playlist2['id']]))) * 100
                similarities.append((playlist1['name'], playlist2['name'], similarity_percentage, len(common_tracks)))

    similarities.sort(key=lambda x: x[2], reverse=True)

    if not similarities:
        print("\nNo similarities found between any playlists.")
        return

    print("\nPlaylist Similarity Analysis:")
    print("------------------------------")
    for playlist1, playlist2, similarity, common_count in similarities:
        print(f"'{playlist1}' and '{playlist2}':")
        print(f"  Similarity: {similarity:.2f}%")
        print(f"  Common tracks: {common_count}")
        print()

    playlist_avg_similarity = defaultdict(list)
    for playlist1, playlist2, similarity, _ in similarities:
        playlist_avg_similarity[playlist1].append(similarity)
        playlist_avg_similarity[playlist2].append(similarity)

    if playlist_avg_similarity:
        most_unique = min(playlist_avg_similarity, key=lambda x: sum(playlist_avg_similarity[x])/len(playlist_avg_similarity[x]))
        most_similar = max(playlist_avg_similarity, key=lambda x: sum(playlist_avg_similarity[x])/len(playlist_avg_similarity[x]))

        print(f"Most unique playlist: '{most_unique}'")
        print(f"Most similar playlist: '{most_similar}'")
    else:
        print("Unable to determine most unique and most similar playlists due to lack of similarities.")
