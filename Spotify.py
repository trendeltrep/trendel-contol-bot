import platform
import subprocess
from aiogram import types


async def spotify_start(path: str, message: types.Message):
    """Start  command handler."""
    try:
        await message.answer("Opening...")
        subprocess.Popen([path])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening : {e}")


async def spotify_close(message: types.Message):
    """Close  command handler."""
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "Spotify.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Spotify"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "Spotify"])
    else:
        print("Unsupported operating system")
