import json
import logging
import os
import functools
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from steam import steam_start, steam_close
from spotify import (
    spotify_start,
    spotify_close,
    search_music,
    play_track,
    pause_music,
    resume_music,
)
from chrome import chrome_open, chrome_close
from pc import (
    take_screenshot,
    take_screenshot_framed,
    close,
    click,
    double_click,
    move_to,
    scroll_page,
    reboot,
    power_off,
)

#
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
CLIENT_ID_SPOTIFY = config["CLIENT_ID_SPOTIFY"]
CLIENT_SECRET_SPOTIFY = config["CLIENT_SECRET_SPOTIFY"]
SPOTIFY_REDIRECT_URI = config["SPOTIFY_REDIRECT_URI"]
SPOTIFY_USERNAME = config["SPOTIFY_USERNAME"]


BOT_PAUSED = False


sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID_SPOTIFY,
    client_secret=CLIENT_SECRET_SPOTIFY,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-library-read user-modify-playback-state user-read-playback-state",
)
sp = Spotify(auth_manager=sp_oauth)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

commands = """
/start - Starting bot
/enable_bot - Enable bot
/pause_bot - Pause bot
/steam_start - Open 
/steam_close - Close 
/spotify_start - Open spotify
/spotify_close - Close spotify
/search_music - Search a music at spotify needs querry
/play_msuic - Needs id track from "/search_music" (spotify:track:*id*) | needs premium
/pause_music - Pause music | needs premium
/resume_music - Resume music | needs premium
/chrome - Open a chrome with querry (need querry inputs) | needs premium
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


# /steam_start
@dp.message_handler(commands=["steam_start"])
@admin_and_not_paused
async def s_start(message: types.Message):
    await steam_start(PATH_TO_STEAM, message)


# /steam_close
@dp.message_handler(commands=["steam_close"])
@admin_and_not_paused
async def s_close(message: types.Message):
    await steam_close(message)


# /spotify_start
@dp.message_handler(commands=["spotify_start"])
@admin_and_not_paused
async def s_start(message: types.Message):
    await spotify_start(PATH_TO_SPOTIFY, message)


# /spotify_close
@dp.message_handler(commands=["spotify_close"])
@admin_and_not_paused
async def s_close(message: types.Message):
    await spotify_close(message)


# /screen
@dp.message_handler(commands=["screen"])
@admin_and_not_paused
async def screen(message: types.Message):
    await take_screenshot(bot, message)


# /screen_framed | /screen_framed *num*
@dp.message_handler(commands=["screen_framed"])
@admin_and_not_paused
async def screen_framed(message: types.Message):
    await take_screenshot_framed(bot, message)


# /chrome *input*
@dp.message_handler(commands=["chrome"])
@admin_and_not_paused
async def c_open(message: types.Message):
    await chrome_open(bot, PATH_TO_CHROME, message)


# /close *any apps in lowercase*
@dp.message_handler(commands=["close"])
@admin_and_not_paused
async def c(message: types.Message):
    await close(message)


# Register a command handler to close browser
# /chrome_close
@dp.message_handler(commands=["chrome_close"])
@admin_and_not_paused
async def c_close(message: types.Message):
    await chrome_close(message)


# Register a command handler to click at exact place
# /click | /click x y
@dp.message_handler(commands=["click"])
@admin_and_not_paused
async def c(message: types.Message):
    await click(message)


# /double_click
@dp.message_handler(commands=["double_click"])
@admin_and_not_paused
async def d_c(message: types.Message):
    await double_click(message)


# Register a command handler to click at exact place
# /move_to x y
@dp.message_handler(commands=["move_to"])
@admin_and_not_paused
async def m_t(message: types.Message):
    await move_to(message)


# Register a command handler to scrolling
# /scroll *num*
@dp.message_handler(commands=["scroll"])
@admin_and_not_paused
async def s_page(message: types.Message):
    await scroll_page(bot, message)


# Register a command handler to reboot the computer
# /reboot
@dp.message_handler(commands=["reboot"])
@admin_and_not_paused
async def r(message: types.Message):
    await reboot(message)


# Register a command handler to power off the computer
# /power_off
@dp.message_handler(commands=["power_off"])
@admin_and_not_paused
async def p_off(message: types.Message):
    await power_off(message)


# /search_music *query*
@dp.message_handler(commands=["search_music"])
@admin_and_not_paused
async def s_music(message: types.Message):
    query = message.text[len("/search_music") :].strip()
    tracks = await search_music(sp, query)
    response = "Search results:\n"
    for i, track in enumerate(tracks, start=1):
        track_name = track.get("name", "Unknown Track")
        artists = ", ".join(
            artist.get("name", "Unknown Artist") for artist in track.get("artists", [])
        )
        uri = track.get("uri", "No URI")
        response += f"{i}. {track_name} - {artists} : {uri}\n"
    await message.answer(response)


# /play *track id from /search_music*
@dp.message_handler(commands=["play_music"])
@admin_and_not_paused
async def play(message: types.Message):
    command_args = message.text.split()
    if len(command_args) != 2:
        await message.answer("Usage: /play_music <track_uri>")
        return

    track_uri = command_args[1]
    success = await play_track(sp, track_uri)

    if success:
        await message.answer("Playback started.")
    else:
        await message.answer("Failed to start playback.")


# /pause_music
@dp.message_handler(commands=["pause_music"])
@admin_and_not_paused
async def p(message: types.Message):
    await pause_music(sp, message)


# /resume_music
@dp.message_handler(commands=["resume_music"])
@admin_and_not_paused
async def r(message: types.Message):
    await resume_music(sp, message)


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
