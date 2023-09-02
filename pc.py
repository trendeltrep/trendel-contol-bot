import os
import platform
import subprocess
import pyautogui
import tempfile
from aiogram import Bot, types
from aiogram.types import InputFile
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_PATH = "screenshot.png"
DEFAULT_GRID_SIZE = 5


async def send_screenshot(bot: Bot, chat_id: int):
    with open(SCREENSHOT_PATH, "rb") as screenshot_file:
        await bot.send_photo(chat_id, screenshot_file)
    os.remove(SCREENSHOT_PATH)


async def take_screenshot(bot: Bot, message: types.Message):
    try:
        pyautogui.screenshot(SCREENSHOT_PATH)
        await send_screenshot(bot, message.chat.id)
    except Exception as e:
        await message.answer(f"Error taking screenshot: {e}")


async def take_screenshot_framed(bot: Bot, message: types.Message):
    try:
        pyautogui.screenshot(SCREENSHOT_PATH)
        image = Image.open(SCREENSHOT_PATH)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        split_result = message.text.split()
        grid_size = (
            int(split_result[1]) if len(split_result) >= 2 else DEFAULT_GRID_SIZE
        )
        if grid_size <= 0:
            grid_size = DEFAULT_GRID_SIZE

        width, height = image.size
        for x in range(0, width, width // grid_size):
            draw.line([(x, 0), (x, height)], fill=(255, 0, 0))
            draw.text((x, 0), str(x), fill=(255, 0, 0), font=font)
        for y in range(0, height, height // grid_size):
            draw.line([(0, y), (width, y)], fill=(255, 0, 0))
            draw.text((0, y), str(y), fill=(255, 0, 0), font=font)

        image.save(SCREENSHOT_PATH)
        await send_screenshot(bot, message.chat.id)
    except Exception as e:
        await message.answer(f"Error taking screenshot: {e}")


async def close_app(message: types.Message):
    apps = message.text.split()[1:]
    for app in apps:
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", f"{app}.exe"])
            await message.answer(f"Closed {app}")
        elif platform.system() == "Darwin":
            subprocess.run(["pkill", "-x", f"{app}"])
            await message.answer(f"Closed {app}")
        elif platform.system() == "Linux":
            subprocess.run(["pkill", f"{app}"])
            await message.answer(f"Closed {app}")
        else:
            print("Unsupported operating system")


async def close(message: types.Message):
    apps = message.text.split()[1:]
    for app in apps:
        await close_app(message, app)


async def click(message: types.Message):
    coords = message.text.split()[1:]
    if len(coords) == 2:
        try:
            x, y = map(int, coords)
            pyautogui.moveTo(x, y)
            pyautogui.click(x, y)
        except ValueError:
            await message.answer("Invalid coordinates. Use /click x y")
    elif len(coords) == 0:
        x, y = pyautogui.position()
        pyautogui.click(x, y)
    else:
        await message.answer("Invalid number of coordinates. Use /click x y")


async def double_click(message: types.Message):
    pyautogui.doubleClick()


async def right_click(message: types.Message):
    pyautogui.rightClick()


async def move_to(message: types.Message):
    coords = message.text.split()[1:]
    if len(coords) == 2:
        try:
            x, y = map(int, coords)
            pyautogui.moveTo(x, y)
        except ValueError:
            await message.answer("Invalid coordinates.")
    else:
        await message.answer("Invalid number of coordinates.")


async def scroll_page(bot: Bot, message: types.Message):
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

        pyautogui.screenshot(SCREENSHOT_PATH)
        await send_screenshot(bot, message.chat.id)
    except (IndexError, ValueError):
        await message.answer("Invalid command format. Use /scroll <value>")


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


async def power_off(message: types.Message):
    shut_time = message.text.split()[1:]
    system = platform.system()

    if len(shut_time) == 1:
        try:
            s_t = int(shut_time[0], 10) * 60
            if system == "Windows":
                subprocess.run(["shutdown", "/s", "/f", "/t", f"{s_t}"], check=True)
            else:
                print("Unsupported operating system")
        except subprocess.CalledProcessError as e:
            print(f"Error powering off: {e}")
    else:
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


async def send_file(bot: Bot, message: types.Message):
    file_path = message.text[len("/send_file") :].strip()
    if os.path.exists(file_path):
        await bot.send_document(message.chat.id, InputFile(file_path))
    else:
        await message.answer("File does not exist.")


async def tree(message: types.Message):
    dir_path = message.text[len("/tree") :].strip()

    # Use a raw string to preserve backslashes in the path

    dir_path = rf"{dir_path}"
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        tree_str = generate_tree(dir_path)

        # Save the tree representation to a temporary text file with a .txt extension
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", encoding="utf-8", suffix=".txt"
        ) as temp_file:
            temp_file.write(tree_str)

        # Send the text file as a document
        with open(temp_file.name, "rb") as document:
            await message.answer_document(document)
    else:
        await message.answer("Directory does not exist.")


def generate_tree(dir_path, padding=""):
    tree_str = padding[:-1] + "+--" + os.path.basename(dir_path) + "/" + "\n"
    padding = padding + " "

    try:
        if os.path.isdir(dir_path):
            for i, child in enumerate(sorted(os.listdir(dir_path))):
                child_path = os.path.join(dir_path, child)
                try:
                    if os.path.isdir(child_path):
                        tree_str += generate_tree(child_path, padding + "|  ")
                    else:
                        tree_str += padding + "|-- " + child + "\n"
                except PermissionError as e:
                    # Handle the PermissionError by skipping the directory/file
                    tree_str += padding + "|-- " + f"PermissionError: {e}" + "\n"
    except PermissionError as e:
        # Handle the PermissionError for the root directory
        tree_str = f"PermissionError: {e}" + "\n"

    return tree_str
