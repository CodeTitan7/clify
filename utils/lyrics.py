import requests
import os
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from .controls import *
from .config import sp
load_dotenv()
def get_lyrics():
    current_song = sp.current_playback()

    if current_song and current_song.get('item'):
        song_name = current_song['item']['name']
        artist = current_song['item']['artists'][0]['name']
        album = current_song['item']['album']['name']
    else:
        print("No song currently playing.")
        return

    genius_token = os.getenv("GENIUS_TOKEN")
    if not genius_token:
        raise ValueError("Genius access token not found in environment variables")

    try:
        search_url = f"https://api.genius.com/search?q={artist} {song_name}&access_token={genius_token}"
        response = requests.get(search_url)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            hits = data['response']['hits']
            if hits:
                lyrics_url = hits[0]['result']['url']
                print(f"Lyrics URL: {lyrics_url}")

                lyrics_page = requests.get(lyrics_url)
                lyrics_page.raise_for_status()

                soup = BeautifulSoup(lyrics_page.text, 'html.parser')
                lyrics_div = soup.find('div', class_=re.compile(r'^Lyrics__Container.*'))
                if lyrics_div:
                    lyrics = lyrics_div.get_text()
                    print(f"Lyrics for {song_name} by {artist}:\n{lyrics}")
                else:
                    print("Lyrics not found on the page.")
            else:
                print("No lyrics found for this song.")
        else:
            print("Failed to search for lyrics.")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while searching for lyrics: {e}")
