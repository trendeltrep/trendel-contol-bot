import json
import logging
import os
import platform
import subprocess
import pyautogui
import time
import functools
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from PIL import Image, ImageDraw, ImageFont


# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration from JSON file
script_directory = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_directory, "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)
# Load configuration from config
API_TOKEN = config["API_TOKEN"]
PATH_TO_STEAM = config["PATH_TO_STEAM"]
PATH_TO_CHROME = config["PATH_TO_CHROME"]
PATH_TO_SPOTIFY = config["PATH_TO_SPOTIFY"]
ADMIN_ID = config["ADMIN_ID"]
BOT_PAUSED = False

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

commands = """
/start - Starting bot
/enable_bot - Enable bot
/pause_bot - Pause bot
/_start - Open 
/_close - Close 
/spotify_start - Open spotify
/spotify_close - Close spotify
/chrome - Open a chrome with querry (need querry inputs)
/chrome_close - Close a chrome
/screen - Send a screen of window on PC
/screen_framed - Screenshot divided into frames
/click - Click at exact place (x,y)
/double_click - LMB doubleclick
/scroll - Scroll up or down (with negative numbers)
/move_to - Move to exact place
/close - Close any app
/reboot - Reboot PC
/power_off - Turn off PC
"""


def is_admin(user_id: int) -> bool:
    """Check if a user is an admin."""
    return user_id == ADMIN_ID


# Handler to send unauthorized message
async def send_unauthorized_message(message: types.Message):
    await message.answer(
        f"You are not authorized to use this bot, your id is: {message.from_user.id}"
    )


def admin_and_not_paused(func):
    @functools.wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        if not is_admin(message.from_user.id):
            await send_unauthorized_message(message)
        elif BOT_PAUSED:
            await message.answer("Bot is currently paused")
        else:
            await func(message, *args, **kwargs)

    return wrapper


# Start handler
@dp.message_handler(commands=["start"])
@admin_and_not_paused
async def cmd_start(message: types.Message):
    """Start command handler."""

    await message.answer("Hello! I'm your bot. Send me a message!")


# Command handlers
# /help
@dp.message_handler(commands=["help"])
@admin_and_not_paused
async def help(message: types.Message):
    """Start command handler."""

    await message.answer(commands)


# /_start
@dp.message_handler(commands=["_start"])
@admin_and_not_paused
async def _start(message: types.Message):
    """Start  command handler."""

    try:
        await message.answer("Opening...")
        subprocess.Popen([PATH_TO_])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening : {e}")


# /_close
@dp.message_handler(commands=["_close"])
@admin_and_not_paused
async def _close(message: types.Message):
    """Close  command handler."""

    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", ".exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", ""])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", ""])
    else:
        print("Unsupported operating system")


# /spotify_start
@dp.message_handler(commands=["spotify_start"])
@admin_and_not_paused
async def spotify_start(message: types.Message):
    """Start  command handler."""

    try:
        await message.answer("Opening...")
        subprocess.Popen([PATH_TO_SPOTIFY])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening : {e}")


# /spotify_close
@dp.message_handler(commands=["spotify_close"])
@admin_and_not_paused
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


# /screen
@dp.message_handler(commands=["screen"])
@admin_and_not_paused
async def take_screenshot(message: types.Message):
    """Take a screenshot and send it command handler."""

    try:
        screenshot_path = "screenshot.png"
        pyautogui.screenshot(screenshot_path)
        with open(screenshot_path, "rb") as screenshot_file:
            await bot.send_photo(message.chat.id, screenshot_file)
        os.remove(screenshot_path)  # Remove the temporary screenshot file
    except Exception as e:
        await message.answer(f"Error taking screenshot: {e}")


# /screen_framed | /screen_framed *num*
@dp.message_handler(commands=["screen_framed"])
@admin_and_not_paused
async def take_screenshot_framed(message: types.Message):
    """Take a screenshot and send it command handler."""

    try:
        screenshot_path = "screenshot.png"
        pyautogui.screenshot(screenshot_path)

        image = Image.open(screenshot_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        split_result = message.text.split()
        if len(split_result) == 1:
            grid_size = 5  # Default grid size
        elif len(split_result) >= 2:
            try:
                num = int(split_result[1])
            except ValueError:
                logging.info("num - not a number")
            grid_size = num if num > 0 else 5
        width, height = image.size

        # Draw vertical lines and add numbers to the corners
        for x in range(0, width, width // grid_size):
            draw.line([(x, 0), (x, height)], fill=(255, 0, 0))
            draw.text((x, 0), str(x), fill=(255, 0, 0), font=font)

        # Draw horizontal lines and add numbers to the corners
        for y in range(0, height, height // grid_size):
            draw.line([(0, y), (width, y)], fill=(255, 0, 0))
            draw.text((0, y), str(y), fill=(255, 0, 0), font=font)

        image.save(screenshot_path)

        with open(screenshot_path, "rb") as screenshot_file:
            await bot.send_photo(message.chat.id, screenshot_file)
        os.remove(screenshot_path)
    except Exception as e:
        await message.answer(f"Error taking screenshot: {e}")


# /chrome *input*
@dp.message_handler(commands=["chrome"])
@admin_and_not_paused
async def chrome_open(message: types.Message):
    query = " ".join(message.text.split()[1:])  # Extract the search query
    search_url = f"https://www.google.com/search?q={query}"
    # Open Google Chrome with the search URL
    subprocess.Popen(
        [PATH_TO_CHROME, "--incognito", search_url]
    )  # Adjust this command based on your system

    await message.answer(f"Searching for '{query}' in Google Chrome...")
    time.sleep(2)  # Delay to allow Chrome to load

    try:
        screenshot_path = "screenshot.png"
        pyautogui.screenshot(screenshot_path)

        image = Image.open(screenshot_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        grid_size = 5
        width, height = image.size

        # Draw vertical lines and add numbers to the corners
        for x in range(0, width, width // grid_size):
            draw.line([(x, 0), (x, height)], fill=(255, 0, 0))
            draw.text((x, 0), str(x), fill=(255, 0, 0), font=font)

        # Draw horizontal lines and add numbers to the corners
        for y in range(0, height, height // grid_size):
            draw.line([(0, y), (width, y)], fill=(255, 0, 0))
            draw.text((0, y), str(y), fill=(255, 0, 0), font=font)

        image.save(screenshot_path)

        with open(screenshot_path, "rb") as screenshot_file:
            await bot.send_photo(message.chat.id, screenshot_file)
        os.remove(screenshot_path)
    except Exception as e:
        await message.answer(f"Error taking screenshot: {e}")


# /close *any apps in lowercase*
@dp.message_handler(commands=["close"])
@admin_and_not_paused
async def close(message: types.Message):
    apps = message.text.split()[1:]
    for app in apps:
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", f"{app}.exe"])
            message.answer(f"Closed {app}")
        elif platform.system() == "Darwin":
            subprocess.run(["pkill", "-x", f"{app}"])
            message.answer(f"Closed {app}")
        elif platform.system() == "Linux":
            subprocess.run(["pkill", f"{app}"])
            message.answer(f"Closed {app}")
        else:
            print("Unsupported operating system")


# Register a command handler to close browser
# /chrome_close
@dp.message_handler(commands=["chrome_close"])
@admin_and_not_paused
async def chrome_close(message: types.Message):
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Google Chrome"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "chrome"])
    else:
        print("Unsupported operating system")


# Register a command handler to click at exact place
# /click | /click x y
@dp.message_handler(commands=["click"])
@admin_and_not_paused
async def click(message: types.Message):
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
    elif len(coords) == 0:  # No coordinates provided, click at current mouse position
        x, y = pyautogui.position()
        # Perform the mouse click
        pyautogui.click(x, y)
    else:
        await message.answer("Invalid number of coordinates. Use /click x y")


# /double_click
@dp.message_handler(commands=["double_click"])
@admin_and_not_paused
async def double_click(message: types.Message):
    pyautogui.doubleClick()


# Register a command handler to click at exact place
# /move_to x y
@dp.message_handler(commands=["move_to"])
@admin_and_not_paused
async def move_to(message: types.Message):
    coords = message.text.split()[1:]  # Extract coordinates
    if len(coords) == 2:
        try:
            x, y = map(int, coords)  # Convert coordinates to integers
            # Move the mouse to the click position (optional)
            pyautogui.moveTo(x, y)
        except ValueError:
            await message.answer("Invalid coordinates.")
    else:
        await message.answer("Invalid number of coordinates.")


# Register a command handler to scrolling
# /scroll *num*
@dp.message_handler(commands=["scroll"])
@admin_and_not_paused
async def scroll_page(message: types.Message):
    """Scroll a specified number of times command handler."""

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


# Register a command handler to reboot the computer
# /reboot
@dp.message_handler(commands=["reboot"])
@admin_and_not_paused
async def reboot(message: types.Message):
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["shutdown", "/r", "/f", "/t", "0"], check=True)
        elif system == "Linux":
            subprocess.run(["reboot"], check=True)
        elif system == "Darwin":
            subprocess.run(["sudo", "reboot"], check=True)
        else:
            print("Unsupported operating system")
    except subprocess.CalledProcessError as e:
        print(f"Error rebooting: {e}")


# Register a command handler to power off the computer
# /power_off
@dp.message_handler(commands=["power_off"])
@admin_and_not_paused
async def power_off(message: types.Message):
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
        elif system == "Linux":
            subprocess.run(["shutdown", "-h", "now"], check=True)
        elif system == "Darwin":
            subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
        else:
            print("Unsupported operating system")
    except subprocess.CalledProcessError as e:
        print(f"Error powering off: {e}")


# /enable_bot
@dp.message_handler(commands=["enable_bot"])
async def enable_bot(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    global BOT_PAUSED
    BOT_PAUSED = False
    await message.answer("Bot enabled")


# /pause_bot
@dp.message_handler(commands=["pause_bot"])
async def pause_bot(message: types.Message):
    global BOT_PAUSED
    BOT_PAUSED = True
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    await message.answer("Bot paused")


# Register a text message handler
@dp.message_handler(content_types=types.ContentTypes.TEXT)
@admin_and_not_paused
async def test(message: types.Message):
    words = message.text.split()[1:]  # Skip the command itself
    for word in words:
        await message.answer(word)


if __name__ == "__main__":
    # Initialize a flag to track whether the bot is paused or not
    BOT_PAUSED = False

    # Start the bot
    executor.start_polling(dp, skip_updates=True)
