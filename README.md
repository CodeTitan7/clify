# CLIFY

A command-line interface (CLI) tool for controlling Spotify playback using the Spotify Web API and Spotipy. This tool allows users to search for tracks, control playback (play, pause, skip, etc.), and set timers, all from the terminal. It is designed to simplify Spotify interaction for power users and developers through an easy-to-use command-line interface.

## Features

1. **Play/Pause**: Start and pause playback.
2. **Next/Previous**: Skip to the next or previous track.
3. **Search**: Search for tracks, albums, or artists on Spotify.
4. **Lyrics**: Fetch and display lyrics for the currently playing track.
5. **Timer**: Set a timer to pause or stop the current track after a specific time.
6. **Playlist Management**: Create and manage playlists.
7. **Device Control**: Switch playback between different devices.
8. **Library Management**: Show and manage saved tracks.
9. **Spotipy Integration**: Leverages the Spotipy library to simplify API interactions.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/CodeTitan7/clify.git
    cd clify
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the `main.py` file:

    ```bash
    python main.py
    ```

4. Use the `Search` command to search a particular song:

    ```bash
    Clify/Search > song_name
    ```

5. Then use play command followed by the song number to play the song

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
