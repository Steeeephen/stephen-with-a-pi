import os

from youtube_playlist_tracker import check_playlist

def main():
    messages = check_playlist(
        os.environ['YOUTUBE_PLAYLIST'],
        old_playlist_location = 'checks/')

    return messages