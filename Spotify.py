import platform
import subprocess
from spotipy import Spotify
from aiogram import types
from spotipy.oauth2 import SpotifyClientCredentials


async def spotify_start(path: str, message: types.Message):
    # Start  command handler.
    try:
        await message.answer("Opening...")
        subprocess.Popen([path])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening : {e}")


async def spotify_close(message: types.Message):
    # Close  command handler.
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "Spotify.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Spotify"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "Spotify"])
    else:
        print("Unsupported operating system")




async def search_music(sp:Spotify,query: str) -> list:
    results = sp.search(q=query, type="track", limit=10)
    tracks = results.get("tracks", {}).get("items", [])
    return tracks

async def play_track(sp: Spotify, uri: str) -> bool:
    try:
        sp.start_playback(uris=[uri])
        return True
    except Exception as e:
        print("Error playing track:", e)
        return False

