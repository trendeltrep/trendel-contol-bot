import logging
import os
import subprocess
import pyautogui
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Your bot's API token (replace 'API_TOKEN' with your actual API token)
API_TOKEN = os.getenv("API_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def is_admin(user_id: int) -> bool:
    return user_id == int(os.getenv("ADMIN"))


def send_unauthorized_message(message: types.Message):
    return f"You are not authorized to use this bot, your id is: {message.from_user.id}"


# Register a command handler
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! I'm your bot. Send me a message!")


# Register a command handler to start Steam
@dp.message_handler(commands=["steam_start"])
async def steam_start(message: types.Message):
    if is_admin(message.from_user.id):
        steam_exe = r"D:\steam\Steam.exe"  # Adjust the path to your Steam executable
        await message.answer("Opening...")
        subprocess.Popen([steam_exe])
        await message.answer("Done")

    else:
        send_unauthorized_message(message)


# Register a command handler to close Steam
@dp.message_handler(commands=["steam_close"])
async def steam_close(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("Closing...")
        subprocess.run(["taskkill", "/F", "/IM", "steam.exe"])
        await message.answer("Done")
    else:
        send_unauthorized_message(message)


# Register a command handler to take a screenshot and send it
@dp.message_handler(commands=["screen"])
async def take_screenshot(message: types.Message):
    if is_admin(message.from_user.id):
        screenshot_path = "screenshot.png"
        pyautogui.screenshot(screenshot_path)
        with open(screenshot_path, "rb") as screenshot_file:
            await bot.send_photo(message.chat.id, screenshot_file)
        os.remove(screenshot_path)  # Remove the temporary screenshot file
    else:
        send_unauthorized_message(message)


# Register a text message handler
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo_message(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer(f"You said: {message.text}")
    else:
        send_unauthorized_message(message)


if __name__ == "__main__":
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
