from .controls import *
from .config import sp
import time


def playlists():
    playlist_items = sp.current_user_playlists()
    if not playlist_items or not playlist_items['items']:
        print("You have no playlists.")
        return
    for i, item in enumerate(playlist_items['items']):
        playlist = item['name']
        print(f"{i}. {playlist}")
    playlist_number = input("Clify/Playlists/Selection >")
    if playlist_number == "back":
        return
    try:
        playlist_number = int(playlist_number)
        selected_playlist = playlist_items['items'][playlist_number]
        playlist_uri = selected_playlist['uri']
        playlists_global(playlist_uri)
    except (IndexError, ValueError):
        print("Sorry, that's an invalid number.")
        playlists()


def show_library(page=1, page_size=10):
    if page is None:
        page = 1
    try:
        page = int(page)
        if page < 1:
            raise ValueError("Page number must be a positive integer.")
    except ValueError as e:
        print(f"Invalid page number. {e}")
        return

    offset = (page - 1) * page_size
    library_items = sp.current_user_saved_tracks(limit=page_size, offset=offset)

    if not library_items or not library_items['items']:
        print("Your library is empty.")
        return
    print(f"Page {page} \n")
    for i, item in enumerate(library_items['items']):
        track = item['track']
        print(f"{i}. {track['name']} by {track['artists'][0]['name']}")

    while True:
        action = input("Clify/Library/Action > ")

        if action == "play":
            track_number = input("Clify/Library/Play > ")
            if track_number == "back":
                return
            try:
                track_number = int(track_number)
            except (ValueError, IndexError) as e:
                print("Error: Invalid track number. Please try again.")
            selected_track = library_items['items'][track_number]
            playback(selected_track['track'])

        elif action == "prev" and library_items['previous']:
            show_library(page - 1, page_size)
            return
        elif action == "next" and library_items['next']:
            show_library(page + 1, page_size)
            return
        elif action == "prev":
            print("Already on the first page.")
        elif action == "next":
            print("No more items in your library.")
        elif action == "back":
            return
        else:
            print("Invalid action. Please try again.")
            continue







def nowplaying(args):
    current_song = sp.current_playback()
    if current_song is not None:
        song_name = current_song['item']['name']
        artists = ', '.join([artist['name'] for artist in current_song['item']['artists']])
        album = current_song['item']['album']['name']
        print(f""" 
Now playing: {song_name} by {artists}.""")
        if "-a" in args:
            print(f"Album: {album}")
        print(" ")
        if "-l" in args:
            sp.current_user_saved_tracks_add([current_song['item']['id']])
            print(f"{current_song['item']['name']} has been added to your library.")

    else:
        print("""
No song currently playing.
        """)

def recs():
    current_song = sp.current_playback()
    if current_song is None:
        print("Sorry, we can't recommend anything until you start playing a song.")
    else:
        track = current_song['item']['uri']
        recs_list = sp.recommendations(seed_tracks=[track])
        for i, t in enumerate(recs_list['tracks']):
            track_name = t['name']
            artists = ', '.join([artist['name'] for artist in t['artists']])
            album = t['album']['name']
            print(f" {i} {track_name} by {artists}")


def spotify_search(args):
    spotify_search_global(args)


def create_playlist(user_profile):
    playlist_name = input("Clify/Playlist/Name > ")
    playlist = sp.user_playlist_create(user=user_profile['id'], name=playlist_name)
    print(f"\nCreated new playlist: {playlist_name}\n")
    print("Would you like to add songs now? (y, or any other input for no.)")
    add_songs_choice = input("Clify/Playlist/Action > ")
    if add_songs_choice == "y":
        while True:
            result = add_songs_playlist(playlist['uri'])
            if result == "back":
                break
            print("Add another? (y, or any other input for no.)")
            choice = input("Clify/Playlist/Action > ")
            if choice == "y":
                continue
            else:
                break


def pause():
    current_playback = sp.current_playback()

    if current_playback is not None:
        if current_playback.get('is_playing', False):
            sp.pause_playback()
            print("Paused")
        else:
            print("Spotify is already paused.")
    else:
        print("Can't pause, there is nothing playing.")


def play():
    current_playback = sp.current_playback()
    if current_playback is not None:
        if current_playback.get('is_playing', False):
            print("Spotify is already playing.")
        else:
            print("Resuming playback.")
            sp.start_playback()
    else:
        recently_played = sp.current_user_recently_played(limit=10)
        if recently_played and 'items' in recently_played:
            track_uris = [item['track']['uri'] for item in recently_played['items']]

            device_id = choose_device()

            if device_id == "back":
                return "back"
            elif device_id is None:
                print("Playback aborted.")
                return

            sp.start_playback(uris=track_uris, device_id=device_id)
            print(f"Playing the most recently played track: {recently_played['items'][0]['track']['name']}")
        else:
            print("No recently played tracks found.")


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
        print("Nothing is playing. Please use the play command or search for a song.")


def prev():
    current_playback = sp.current_playback()

    if current_playback is not None:
        disallowPrevSkip = current_playback['actions']['disallows'].get('skipping_prev')

        if not disallowPrevSkip:
            sp.previous_track()

            for _ in range(10):
                updated_playback = sp.current_playback()
                if (
                    updated_playback is not None
                    and updated_playback['item'].get('uri') != current_playback['item'].get('uri')
                ):
                    break
                time.sleep(0.5)

            nowplaying("")
        elif (disallowPrevSkip):
            print("Can't go back any further. Restarting the current song.")
            playback(current_playback['item'])
    else:
        print("Nothing is playing. Please use the play command or search for a song.")

def shuffle():
    current_playback = sp.current_playback()

    if current_playback is not None:
        current_shuffle_state = current_playback["shuffle_state"]

        if current_shuffle_state is True:
            sp.shuffle(False)
            print("Shuffle disabled.")
        else:
            sp.shuffle(True)
            print("Shuffle enabled.")
    else:
        print("Nothing is playing. Please use the play command before using shuffle.")


def loop(state):
    try:
        sp.repeat(state=state)
    except sp.SpotifyException:
        print("Sorry, that didn't work. Remember you need to add the state and make sure music is already playing.")

def timer():
    print("Enter the time in the format HH:MM:SS")
    time_input = input("Clify/Timer > ")
    hour, minutes, seconds = map(int, time_input.split(':'))
    total_seconds = (hour * 60 * 60) + (minutes * 60) + seconds
    mins, secs = divmod(total_seconds, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    print(f"Timer set for {timeformat}")
    time.sleep(total_seconds)
    pause()
    print("Timer finished.")
    