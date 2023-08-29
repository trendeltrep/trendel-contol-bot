import platform
import subprocess
from aiogram import types


async def steam_start(path: str, message: types.Message):
    # Start Steam command handler.

    try:
        await message.answer("Opening...")
        subprocess.Popen([path])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening Steam: {e}")


async def steam_close(message: types.Message):
    # Close Steam command handler.

    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "steam.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Steam"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "steam"])
    else:
        print("Unsupported operating system")
