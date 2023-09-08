import datetime
import logging
import functools
import statistic

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from vsc import vsc_start, vsc_close
from loading import get_commands, get_config
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
    close_app,
    send_file,
    tree,
    click,
    double_click,
    right_click,
    move_to,
    scroll_page,
    reboot,
    power_off,
)

# Set up logging
logging.basicConfig(level=logging.INFO)

commands = get_commands().items()
config = get_config()
try:
    data = statistic.load()
except Exception as e:
    logging.error(e)
# Load configuration from config
API_TOKEN = config["API_TOKEN"]
PATH_TO_STEAM = config["PATH_TO_STEAM"]
PATH_TO_CHROME = config["PATH_TO_CHROME"]
PATH_TO_VSC = config["PATH_TO_VSC"]
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
        logging.info(
            f" {datetime.datetime.now()} - {func.__name__} | {message.from_user.username} : {message.from_user.id} | {message.text}"
        )
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
async def start(message: types.Message):
    """Start command handler."""
    await message.answer("Hello! I'm your bot. Send me a message!")
    data["start"] += 1


# Command handlers
# /help
@dp.message_handler(commands=["help"])
@admin_and_not_paused
async def send_commands(message: types.Message):
    """Start command handler."""
    msg = ""
    for com, desc in commands:
        msg += f"/{com} : {desc} \n"
    pin_msg = await message.answer(msg)
    await bot.pin_chat_message(message.chat.id, pin_msg.message_id)
    data["help"] += 1


# /vsc_start
@dp.message_handler(commands=["vsc_start"])
@admin_and_not_paused
async def pc_vsc_start(message: types.Message):
    await vsc_start(PATH_TO_VSC, message)
    data["vsc_start"] += 1


# /vsc_close
@dp.message_handler(commands=["vsc_close"])
@admin_and_not_paused
async def pc_vsc_close(message: types.Message):
    await vsc_close(message)
    data["vsc_close"] += 1


# /steam_start
@dp.message_handler(commands=["steam_start"])
@admin_and_not_paused
async def pc_steam_start(message: types.Message):
    await steam_start(PATH_TO_STEAM, message)
    data["steam_start"] += 1


# /steam_close
@dp.message_handler(commands=["steam_close"])
@admin_and_not_paused
async def pc_steam_close(message: types.Message):
    await steam_close(message)
    data["steam_close"] += 1


# /spotify_start
@dp.message_handler(commands=["spotify_start"])
@admin_and_not_paused
async def pc_spotify_close(message: types.Message):
    await spotify_start(PATH_TO_SPOTIFY, message)
    data["spotify_start"] += 1


# /spotify_close
@dp.message_handler(commands=["spotify_close"])
@admin_and_not_paused
async def pc_spotify_close(message: types.Message):
    await spotify_close(message)
    data["spotify_close"] += 1


# /send_file *path*
@dp.message_handler(commands=["send_file"])
@admin_and_not_paused
async def pc_send_file(message: types.Message):
    await send_file(bot, message)
    data["send_file"] += 1


# /tree *path*
@dp.message_handler(commands=["tree"])
@admin_and_not_paused
async def pc_tree(message: types.Message):
    await tree(message)
    data["tree"] += 1


# /screen
@dp.message_handler(commands=["screen"])
@admin_and_not_paused
async def pc_screen(message: types.Message):
    await take_screenshot(bot, message)
    data["screen"] += 1


# /screen_framed | /screen_framed *num*
@dp.message_handler(commands=["screen_framed"])
@admin_and_not_paused
async def pc_screen_f(message: types.Message):
    await take_screenshot_framed(bot, message)
    data["screen_framed"] += 1


# /chrome *input*
@dp.message_handler(commands=["chrome"])
@admin_and_not_paused
async def pc_chrome_open(message: types.Message):
    await chrome_open(bot, PATH_TO_CHROME, message)
    data["chrome"] += 1


# /close *any apps in lowercase*
@dp.message_handler(commands=["close"])
@admin_and_not_paused
async def pc_close(message: types.Message):
    await close_app(message)
    data["close"] += 1


# Register a command handler to close browser
# /chrome_close
@dp.message_handler(commands=["chrome_close"])
@admin_and_not_paused
async def pc_chrome_close(message: types.Message):
    await chrome_close(message)
    data["chrome_close"] += 1


# Register a command handler to click at exact place
# /click | /click x y
@dp.message_handler(commands=["click"])
@admin_and_not_paused
async def pc_lmb(message: types.Message):
    await click(message)
    data["click"] += 1


# /double_click
@dp.message_handler(commands=["double_click"])
@admin_and_not_paused
async def pc_double_click(message: types.Message):
    await double_click(message)
    data["double_click"] += 1


# /right_click
@dp.message_handler(commands=["right_click"])
@admin_and_not_paused
async def pc_rmb(message: types.Message):
    await right_click(message)
    data["right_click"] += 1


# /move_to | /move_to x y
@dp.message_handler(commands=["move_to"])
@admin_and_not_paused
async def pc_move_to(message: types.Message):
    await move_to(message)
    data["move_to"] += 1


# /scroll_page | /scroll_page *num*
@dp.message_handler(commands=["scroll"])
@admin_and_not_paused
async def pc_scroll(message: types.Message):
    await scroll_page(bot, message)
    data["scroll"] += 1


# /reboot
@dp.message_handler(commands=["reboot"])
@admin_and_not_paused
async def pc_reboot(message: types.Message):
    await reboot(message)
    data["reboot"] += 1


# /power_off | /power_off *num*
@dp.message_handler(commands=["power_off"])
@admin_and_not_paused
async def pc_power_off(message: types.Message):
    await power_off(message)
    data["power_off"] += 1


# /search_music *query*
@dp.message_handler(commands=["search_music"])
@admin_and_not_paused
async def spotify_search(message: types.Message):
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
    data["search_music"] += 1


# /play *track id from /search_music*
@dp.message_handler(commands=["play_music"])
@admin_and_not_paused
async def spotify_play(message: types.Message):
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
    data["play_music"] += 1


# /pause_music
@dp.message_handler(commands=["pause_music"])
@admin_and_not_paused
async def spotify_pause_music(message: types.Message):
    await pause_music(sp, message)
    data["pause_music"] += 1


# /resume_music
@dp.message_handler(commands=["resume_music"])
@admin_and_not_paused
async def spotify_resume_music(message: types.Message):
    await resume_music(sp, message)
    data["resume_music"] += 1


# /statics
@dp.message_handler(commands=["statistic"])
@admin_and_not_paused
async def show_statistic(message: types.Message):
    await statistic.send_statistic(data.items(), message)
    data["statistic"] += 1


# /enable_bot
@dp.message_handler(commands=["enable_bot"])
async def enable_bot(message: types.Message):
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    global BOT_PAUSED
    BOT_PAUSED = False
    await message.answer("Bot enabled")
    data["enable_bot"] += 1


# /pause_bot
@dp.message_handler(commands=["pause_bot"])
async def pause_bot(message: types.Message):
    global BOT_PAUSED
    BOT_PAUSED = True
    if not is_admin(message.from_user.id):
        await send_unauthorized_message(message)
        return
    await message.answer("Bot paused")
    data["pause_bot"] += 1


# Register a text message handler
@dp.message_handler(content_types=types.ContentTypes.TEXT)
@admin_and_not_paused
async def send_msg(message: types.Message):
    await message.answer(message.from_user.id)


if __name__ == "__main__":
    # Initialize a flag to track whether the bot is paused or not
    BOT_PAUSED = False
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
    statistic.save_data(data)
