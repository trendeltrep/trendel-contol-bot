import platform
import subprocess
from aiogram import types


async def vsc_start(path: str, message: types.Message):
    try:
        await message.answer("Opening...")
        subprocess.Popen([path])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening Steam: {e}")


async def vsc_close(message: types.Message):
    try:
        await message.answer("Closing...")
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "Code.exe"])
        elif platform.system() == "Darwin":
            subprocess.run(["pkill", "-x", "Visual Studio Code"])
        elif platform.system() == "Linux":
            subprocess.run(["pkill", "code"])
        else:
            await message.answer("Unsupported operating system")
            return
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error closing VSC: {e}")
