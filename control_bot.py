import logging, os, platform, subprocess, pyautogui, time
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from PIL import Image, ImageDraw, ImageFont


# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration from environment variables
API_TOKEN = os.getenv("API_TOKEN")
PATH_TO_STEAM = os.getenv("PATH_TO_STEAM")
PATH_TO_CHROME = os.getenv("PATH_TO_CHROME")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
BOT_PAUSED = False

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
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
    await message.answer("Hello! I'm your bot. Send me a message!")


@dp.message_handler(commands=["steam_start"])
async def steam_start(message: types.Message):
    """Start Steam command handler."""
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
    try:
        await message.answer("Opening...")
        subprocess.Popen([PATH_TO_STEAM])
        await message.answer("Done")
    except Exception as e:
        await message.answer(f"Error opening Steam: {e}")


@dp.message_handler(commands=["steam_close"])
async def steam_close(message: types.Message):
    """Close Steam command handler."""
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "steam.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Steam"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "steam"])
    else:
        print("Unsupported operating system")


@dp.message_handler(commands=["screen"])
async def take_screenshot(message: types.Message):
    """Take a screenshot and send it command handler."""
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
    try:
        screenshot_path = "screenshot.png"
        pyautogui.screenshot(screenshot_path)
        with open(screenshot_path, "rb") as screenshot_file:
            await bot.send_photo(message.chat.id, screenshot_file)
        os.remove(screenshot_path)  # Remove the temporary screenshot file
    except Exception as e:
        await message.answer(f"Error taking screenshot: {e}")


@dp.message_handler(commands=["screen_framed"])
async def take_screenshot_framed(message: types.Message):
    """Take a screenshot and send it command handler."""
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
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


@dp.message_handler(commands=["chrome"])
async def chrome_open(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return

    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
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


@dp.message_handler(commands=["close"])
async def close(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
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
@dp.message_handler(commands=["chrome_close"])
async def chrome_close(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Google Chrome"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "chrome"])
    else:
        print("Unsupported operating system")


# Register a command handler to click at exact place
@dp.message_handler(commands=["click"])
async def click(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return

    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
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


@dp.message_handler(commands=["double_click"])
async def double_click(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
    pyautogui.doubleClick()


# Register a command handler to click at exact place
@dp.message_handler(commands=["move_to"])
async def move_to(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return

    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
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
@dp.message_handler(commands=["scroll"])
async def scroll_page(message: types.Message):
    """Scroll a specified number of times command handler."""
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return

    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
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


# Register a command handler to power off the computer
@dp.message_handler(commands=["power_off"])
async def power_off(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    if BOT_PAUSED:
        await message.answer("Bot is currently paused")
        return
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


@dp.message_handler(commands=["enable_bot"])
async def enable_bot(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    global BOT_PAUSED
    BOT_PAUSED = False


@dp.message_handler(commands=["disable_bot"])
async def disable_bot(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    global BOT_PAUSED
    BOT_PAUSED = True


# Register a text message handler
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def test(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    words = message.text.split()[1:]  # Skip the command itself
    for word in words:
        await message.answer(word)


if __name__ == "__main__":
    # Initialize a flag to track whether the bot is paused or not
    BOT_PAUSED = False

    # Start the bot
    executor.start_polling(dp, skip_updates=True)
