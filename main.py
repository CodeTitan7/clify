from utils import commands
import spotipy
from utils.config import sp
from colorama import Fore, Style


def main():
    global user_profile
    print(Fore.GREEN + """ 
 ## ##   ####       ####   ### ###  ##  ##   
##   ##   ##         ##     ##  ##  ##  ##   
##        ##         ##     ##      ##  ##   
##        ##         ##     ## ##    ## ##   
##        ##         ##     ##        ##     
##   ##   ##  ##     ##     ##        ##     
 ## ##   ### ###    ####   ####       ##     
                                             
 """ + Style.RESET_ALL)
    try:
        user_profile = sp.current_user()
        print("Successfully authenticated. User profile:")
        print(f"Display name: {user_profile['display_name']}")
        print(f"User ID: {user_profile['id']}")

    except spotipy.SpotifyException as e:
        print(f"Error accessing Spotify API: {e}")
    while True:

        try:
            user_input = input("Clify > ")
            if user_input.split()[0] == "nowplaying":
                commands.nowplaying(user_input.split())
            elif user_input == "pause":
                commands.pause()
            elif user_input == "play":
                commands.play()
            elif user_input == "skip":
                commands.skip()
            elif user_input == "shuffle":
                commands.shuffle()
            elif user_input == "timer":
                commands.timer()
            elif user_input.split()[0] == "loop":
                commands.loop(user_input.split()[1])
            elif user_input == "close":
                break
            elif user_input == "help":
                print("""=== HELP ===""")
            else:
                print("Not a command! Type 'help' for a list of commands.")
        except (ValueError, IndexError) as e:
            print(f"An error has occured: {e}")

if __name__ == "__main__":
    main()
