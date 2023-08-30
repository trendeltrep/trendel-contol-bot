import json


async def get_commands():
    with open("commands.json", "r") as json_file:
        commands_data = json.load(json_file)

    commands_dict = {}
    for command, description in commands_data.items():
        commands_dict[command] = description

    return commands_dict
