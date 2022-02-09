import pickle
import sys

from youtubesearchpython import Playlist

def check_playlist(playlist_url, old_playlist_location='.'):
    new_playlist = get_current_playlist(playlist_url)

    old_playlist_location += '/old_playlist.pkl'

    try:
        with open(old_playlist_location, 'rb') as file:
            old_playlist = pickle.load(file)
    except FileNotFoundError:
        old_playlist = new_playlist

    removed_video_ids = check_removed_videos(old_playlist, new_playlist)

    removed_video_titles = [video['title'] for video in old_playlist.videos if video['id'] in removed_video_ids]

    with open(old_playlist_location, 'wb') as file:
        pickle.dump(new_playlist, file)

    return removed_video_titles

def get_current_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    
    while playlist.hasMoreVideos:
        playlist.getNextVideos()
        
    return playlist

def check_removed_videos(old_playlist, new_playlist):
    old_ids = [video['id'] for video in old_playlist.videos]
    new_ids = [video['id'] for video in new_playlist.videos]
    
    removed_video_ids = list(set(old_ids) - set(new_ids))
    
    return removed_video_ids

if __name__ == '__main__':
    check_playlist(sys.argv[1])