from .controls import *
from .config import sp
import time



def nowplaying(args):
    current_song = sp.current_playback()
    if current_song is not None:
        song_name = current_song['item']['name']
        artists = ', '.join([artist['name'] for artist in current_song['item']['artists']])
        album = current_song['item']['album']['name']
        print(f"""now playing: {song_name} by {artists}.""")
        if "-a" in args:
            print(f"album: {album}")
        print(" ")
        if "-l" in args:
            sp.current_user_saved_tracks_add([current_song['item']['id']])
            print(f"{current_song['item']['name']} added")

    else:
        print("no song playing")


def pause():
    current_playback = sp.current_playback()

    if current_playback is not None:
        if current_playback.get('is_playing', False):
            sp.pause_playback()
            print("paused")
        else:
            print("already paised")
    else:
        print("not playing")


def play():
    current_playback = sp.current_playback()
    if current_playback is not None:
        if current_playback.get('is_playing', False):
            print("already playing")
        else:
            print("playing")
            sp.start_playback()
    else:
        recently_played = sp.current_user_recently_played(limit=10)
        if recently_played and 'items' in recently_played:
            track_uris = [item['track']['uri'] for item in recently_played['items']]

            device_id = choose_device()

            if device_id == "back":
                return "back"
            elif device_id is None:
                print("stopped")
                return

            sp.start_playback(uris=track_uris, device_id=device_id)
            print(f"playing recently played track {recently_played['items'][0]['track']['name']}")
        else:
            print("no tracks found")


def skip():
    current_playback = sp.current_playback()

    if current_playback is not None:
        sp.next_track()

        for _ in range(10):
            updated_playback = sp.current_playback()
            if updated_playback is not None and updated_playback['item'].get('uri') != current_playback['item'].get('uri'):
                break
            time.sleep(0.5)

        nowplaying("")
    else:
        print("Nothing")


def shuffle():
    current_playback = sp.current_playback()

    if current_playback is not None:
        current_shuffle_state = current_playback["shuffle_state"]

        if current_shuffle_state is True:
            sp.shuffle(False)
            print("shuffle disabled.")
        else:
            sp.shuffle(True)
            print("shuffle enabled.")
    else:
        print("not playing")


def loop(state):
    try:
        sp.repeat(state=state)
    except sp.SpotifyException:
        print("error")


def timer(hour=0, minutes=0, seconds=5):
    print("Enter the time in the format HH:MM:SS")
    total_seconds = (hour * 60 * 60) + (minutes * 60) + seconds
    mins, secs = divmod(total_seconds, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    print(timeformat, end='\r')
    time.sleep(total_seconds)
    print("Timer finished.")
    pause()
            
        




