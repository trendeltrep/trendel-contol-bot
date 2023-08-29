import logging
import os
import platform
import subprocess
import pyautogui
from aiogram import Bot, types
from PIL import Image, ImageDraw, ImageFont


async def take_screenshot(bot: Bot, message: types.Message):

    # Take a screenshot and send it command handler.
    try:
        screenshot_path = "screenshot.png"
        pyautogui.screenshot(screenshot_path)
        with open(screenshot_path, "rb") as screenshot_file:
            await bot.send_photo(message.chat.id, screenshot_file)
        os.remove(screenshot_path)  # Remove the temporary screenshot file
    except Exception as e:
        await message.answer(f"Error taking screenshot: {e}")


async def take_screenshot_framed(bot: Bot, message: types.Message):

    # Take a screenshot and send it command handler.

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


async def close(message: types.Message):
    # 
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


async def click(message: types.Message):
    # 
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

async def double_click(message: types.Message):
    # 
    pyautogui.doubleClick()

async def move_to(message: types.Message):
    # 
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

async def scroll_page(bot:Bot,message: types.Message):
    # Scroll a specified number of times command handler.

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

async def reboot(message: types.Message):
    # 
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

async def power_off(message: types.Message):\
    # 
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
