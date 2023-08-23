import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import os
import subprocess

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Your bot's API token (replace 'API_TOKEN' with your actual API token)
API_TOKEN = os.getenv("API_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def check(id: int) -> bool:
    result: bool = False
    if id != int(os.getenv("ADMIN")):
        return result
    return not result


# Register a command handler
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! I'm your bot. Send me a message!")


@dp.message_handler(commands=["steam"])
async def steam_start(message: types.Message):
    if check(message.from_user.id) == False:
        await message.answer(
            f"You are not available to use this bot, your id is: {message.from_user.id}"
        )
    else:
        steam_exe = r"D:\steam\Steam.exe"  # Adjust the path to your Steam executable
        subprocess.Popen([steam_exe])


# Register a text message handler
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo_message(message: types.Message):
    if check(message.from_user.id) == False:
        await message.answer(
            f"You are not available to use this bot, your id is: {message.from_user.id}"
        )
    else:
        await message.answer(f"You said: {message.from_user.id}")


if __name__ == "__main__":
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
