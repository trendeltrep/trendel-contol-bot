import platform
import subprocess
from aiogram import types


async def vsc_start(path: str, message: types.Message):
    # Start Steam command handler.

    try:
        await message.answer("Opening...")
        subprocess.Popen([path])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening Steam: {e}")


async def vsc_close(message: types.Message):
    # Start Steam command handler.

    await message.answer("vsc_close not done yet")
