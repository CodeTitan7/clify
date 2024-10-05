import spotipy
from .config import sp
import time


def choose_device():
    devices = sp.devices()
    if not devices['devices']:
        print("no devices")
        return None

    print("device:")
    for i, device in enumerate(devices['devices']):
        print(f"{i}. {device['name']} ({device['id']})")


    while True:
        try:
            device_number = input("Clify/Playback/Choose Device > ")
            if device_number.lower() == "back":
                return "back"

            device_number = int(device_number)
            selected_device_id = devices['devices'][device_number]['id']
            return selected_device_id
        except (ValueError, IndexError):
            print("Invalid input")


