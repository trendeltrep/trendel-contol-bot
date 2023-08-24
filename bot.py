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

# Load configuration from environment variables
API_TOKEN = os.getenv("API_TOKEN")
PATH_TO_STEAM = os.getenv("PATH_TO_STEAM")
PATH_TO_CHROME = os.getenv("PATH_TO_CHROME")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def is_admin(user_id: int) -> bool:
    """Check if a user is an admin."""
    return user_id == ADMIN_ID


# Handler to send unauthorized message
async def send_unauthorized_message(message: types.Message):
    await message.answer(
        f"You are not authorized to use this bot, your id is: {message.from_user.id}"
    )


# Command handlers
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    """Start command handler."""
    await message.answer("Hello! I'm your bot. Send me a message!")


@dp.message_handler(commands=["steam_start"])
async def steam_start(message: types.Message):
    """Start Steam command handler."""
    if is_admin(message.from_user.id):
        try:
            await message.answer("Opening...")
            subprocess.Popen([PATH_TO_STEAM])
            await message.answer("Done")
        except Exception as e:
            await message.answer(f"Error opening Steam: {e}")
    else:
        await send_unauthorized_message(message)


@dp.message_handler(commands=["steam_close"])
async def steam_close(message: types.Message):
    """Close Steam command handler."""
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
        await send_unauthorized_message(message)


@dp.message_handler(commands=["screen"])
async def take_screenshot(message: types.Message):
    """Take a screenshot and send it command handler."""
    if is_admin(message.from_user.id):
        try:
            screenshot_path = "screenshot.png"
            pyautogui.screenshot(screenshot_path)
            with open(screenshot_path, "rb") as screenshot_file:
                await bot.send_photo(message.chat.id, screenshot_file)
            os.remove(screenshot_path)  # Remove the temporary screenshot file
        except Exception as e:
            await message.answer(f"Error taking screenshot: {e}")
    else:
        await send_unauthorized_message(message)


# Register a command handler to open a browser for searching information
@dp.message_handler(commands=["chrome"])
async def chrome_open(message: types.Message):
    if is_admin(message.from_user.id):
        query = " ".join(message.text.split()[1:])  # Extract the search query
        search_url = f"https://www.google.com/search?q={query}"
        # Open Google Chrome with the search URL
        subprocess.Popen(
            [PATH_TO_CHROME, "--incognito", search_url]
        )  # Adjust this command based on your system

        await message.answer(f"Searching for '{query}' in Google Chrome...")
    else:
        send_unauthorized_message(message)


# Register a command handler to close browser
@dp.message_handler(commands=["chrome_close"])
async def chrome_close(message: types.Message):
    if is_admin(message.from_user.id):
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"])
        elif platform.system() == "Darwin":
            subprocess.run(["pkill", "-x", "Google Chrome"])
        elif platform.system() == "Linux":
            subprocess.run(["pkill", "chrome"])
        else:
            print("Unsupported operating system")
    else:
        send_unauthorized_message(message)


# Register a command handler to click at exact place
@dp.message_handler(commands=["click"])
async def click(message: types.Message):
    if is_admin(message.from_user.id):
        coords = message.text.split()[1:]  # Extract coordinates
        if len(coords) == 2:
            try:
                x, y = map(int, coords)  # Convert coordinates to integers
                # Move the mouse to the click position (optional)
                pyautogui.moveTo(x, y)
                # Perform the mouse click
                pyautogui.click(x, y)
            except ValueError:
                await message.answer("Invalid coordinates. Use /click x y")
        else:
            await message.answer("Invalid number of coordinates. Use /click x y")
    else:
        send_unauthorized_message(message)


@dp.message_handler(commands=["scroll"])
async def scroll_page(message: types.Message):
    """Scroll a specified number of times command handler."""
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return

    try:
        scroll_value = int(message.text.split()[1])
        screen_height = pyautogui.size().height
        scroll_distance = screen_height // 2

        direction = -1 if scroll_value > 0 else 1
        abs_scroll_value = abs(scroll_value)

        for _ in range(abs_scroll_value):
            pyautogui.scroll(direction * scroll_distance)
        await message.answer(
            f"Scrolled {'down' if direction == -1 else 'up'} {abs_scroll_value} times."
        )

        try:
            screenshot_path = "screenshot.png"
            pyautogui.screenshot(screenshot_path)
            with open(screenshot_path, "rb") as screenshot_file:
                await bot.send_photo(message.chat.id, screenshot_file)
            os.remove(screenshot_path)
        except Exception as e:
            await message.answer(f"Error taking screenshot: {e}")

    except (IndexError, ValueError):
        await message.answer("Invalid command format. Use /scroll <value>")


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
