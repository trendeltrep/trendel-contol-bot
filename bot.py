import logging
import os
import platform
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
PATH_TO_STEAM = os.getenv("PATH_TO_STEAM")

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
        # Adjust the path to your Steam executable
        await message.answer("Opening...")
        subprocess.Popen([PATH_TO_STEAM])
        await message.answer("Done")

    else:
        send_unauthorized_message(message)


# Register a command handler to close Steam
@dp.message_handler(commands=["steam_close"])
async def steam_close(message: types.Message):
    if is_admin(message.from_user.id):
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "steam.exe"])
        elif platform.system() == "Darwin":
            subprocess.run(["pkill", "-x", "Steam"])
        elif platform.system() == "Linux":
            subprocess.run(["pkill", "steam"])
        else:
            print("Unsupported operating system")
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


# Opening a browser for searching information
@dp.message_handler(commands=["chrome"])
async def chrome_open(message: types.Message):
    if is_admin(message.from_user.id):
        query = " ".join(message.text.split()[1:])  # Extract the search query
        search_url = f"https://www.google.com/search?q={query}"

        # Open Google Chrome with the search URL
        subprocess.Popen(
            ["chrome", search_url]
        )  # Adjust this command based on your system

        await message.answer(f"Searching for '{query}' in Google Chrome...")
    else:
        send_unauthorized_message(message)


# Closing browser
@dp.message_handler(commands=["chrome_close"])
def chrome_close():
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Google Chrome"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "chrome"])
    else:
        print("Unsupported operating system")


# Register a text message handler
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def test(message: types.Message):
    if is_admin(message.from_user.id):
        words = message.text.split()[1:]  # Skip the command itself
        for word in words:
            await message.answer(word)
    else:
        send_unauthorized_message(message)


if __name__ == "__main__":
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
