# PC Control Telegram Bot

This is a Telegram bot that allows you to control various functions on your PC, such as opening applications, taking screenshots, clicking at specific locations, and more.

## Setup and Configuration

1. Clone this repository to your local machine. `git clone https://github.com/trendeltrep/trendel-contol-bot.git`

2. Install the required dependencies using the following command: `pip3 install -r requirements.txt`

3. Create a `config.json` file in the root directory of the project with the following structure:

```json
{
    "API_TOKEN": "YOUR_TELEGRAM_BOT_API_TOKEN",
    "PATH_TO_STEAM": "PATH_TO_STEAM_EXECUTABLE",
    "PATH_TO_CHROME": "PATH_TO_CHROME_EXECUTABLE",
    "PATH_TO_SPOTIFY": "PATH_TO_SPOTIFY_EXECUTABLE",
    "ADMIN_ID": YOUR_TELEGRAM_USER_ID,
    "CLIENT_ID_SPOTIFY": "YOUR_SPOTIFY_CLIENT_ID",
    "CLIENT_SECRET_SPOTIFY": "YOUR_SPOTIFY_CLIENT_SECRET",
    "SPOTIFY_REDIRECT_URI": "YOUR_SPOTIFY_REDIRECT_URI",
    "SPOTIFY_USERNAME": "YOUR_SPOTIFY_USERNAME"
}
```

4. Replace the placeholders with your actual values

5. Start the bot by running the following command: `python control_bot.py`

6. Interact with the bot by sending commands to your bot on Telegram.

## Available Commands

- /start: Start the bot.
- /help: Display available commands and their usage.
- /enable_bot: Enable the bot (admin only).
- /pause_bot: Pause the bot (admin only).
- /steam_start: Open Steam.
- /steam_close: Close Steam.
- /spotify_start: Open Spotify.
- /spotify_close: Close Spotify.
- /search_music <query>: Search for music on Spotify.
- /play_music <track_uri>: Play a track on Spotify.
- /pause_music: Pause music playback on Spotify.
- /resume_music: Resume music playback on Spotify.
- /chrome <query>: Open Chrome with a specific query.
- /chrome_close: Close Chrome.
- /screen: Take a screenshot of the current window.
- /screen_framed: Take a framed screenshot of the current window.
- /click <x> <y>: Simulate a click at the specified coordinates.
- /double_click <x> <y>: Simulate a double click at the specified coordinates.
- /move_to <x> <y>: Move the cursor to the specified coordinates.
- /scroll <num>: Scroll the page up or down by the given amount.
- /close <app_name>: Close a specific application.
- /reboot: Reboot the PC.
- /power_off: Turn off the PC.

## Installing a .exe file via pyinstaller

1. Run the following command to generate a .spec file for your script: `pyinstaller control_bot.py`

This will generate a control_bot.spec file in the same directory as your script.

2. Open the control_bot.spec file using a text editor.

3. Locate the datas list in the .spec file (it will be in a = Analysis()). It will look something like this:

```
List of data files and tuples to include
[('source', 'destination'), ...]
```

<pre>
datas = []
</pre>

4. Add your data files and their corresponding destination paths to the datas list. Each entry in the list should be a tuple containing the source file and the destination directory.

For example, to include "config.json", "pc.py", "spotify.py", "chrome.py", and "steam.py" from the current directory, you would add the following lines:

<pre>
datas = [
    ('config.json', '.'),
    ('pc.py', '.'),
    ('spotify.py', '.'),
    ('chrome.py', '.'),
    ('steam.py', '.'),
]
</pre>

Make sure to adjust the file names and paths according to your project structure.

5. Save the .spec file.

6. Build the executable using the modified .spec file: `pyinstaller control_bot.spec`
