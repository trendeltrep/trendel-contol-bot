import json
import loading

from aiogram import types

stat_file = "statistic.json"
command_file = "commands.json"


def load():
    try:
        with open(command_file, "r") as commands_file:
            commands_data = json.load(commands_file)

        with open(stat_file, "r") as statics_file:
            statics_data = json.load(statics_file)

        # Check if commands_data is similar to statics_data
        if set(commands_data.keys()) == set(statics_data.keys()):
            return statics_data
        else:
            # If not similar, update statics_data with new commands from commands_data
            for command in commands_data:
                if command not in statics_data:
                    statics_data[command] = 0

            # Save the updated statics_data
            with open("statics.json", "w") as statics_file:
                json.dump(statics_data, statics_file)
            return statics_data

    except FileNotFoundError:
        with open("statics.json", "w") as file:
            data = loading.get_commands()
            data_used = {used: 0 for used in data}
            json.dump(data_used, file)
            return data_used


# Saving data to statics.json
def save_data(save_d):
    with open(stat_file, "w") as file:
        json.dump(save_d, file)


# Resetting data to default
def reset_data():
    with open(stat_file, "w") as file:
        data = loading.get_commands()
        data_used = {used: 0 for used in data}
        json.dump(data_used, file)


async def send_statistic(data, message: types.Message):
    res = ""
    for com, time in data:
        res += f"/{com} | used {time} times\n"
    await message.answer(res)
