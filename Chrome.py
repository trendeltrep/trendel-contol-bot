import os
import platform
import subprocess
import time
import pyautogui
from aiogram import Bot, types
from PIL import Image, ImageDraw, ImageFont


async def chrome_open(bot: Bot, path: str, message: types.Message):
    query = " ".join(message.text.split()[1:])  # Extract the search query
    search_url = f"https://www.google.com/search?q={query}"
    # Open Google Chrome with the search URL
    subprocess.Popen(
        [path, "--incognito", search_url]
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


async def chrome_close(message: types.Message):
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"])
    elif platform.system() == "Darwin":
        subprocess.run(["pkill", "-x", "Google Chrome"])
    elif platform.system() == "Linux":
        subprocess.run(["pkill", "chrome"])
    else:
        print("Unsupported operating system")
