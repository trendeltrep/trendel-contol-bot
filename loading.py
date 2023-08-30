import json
import os


def get_commands():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    commands_path = os.path.join(script_directory, "commands.json")
    with open(commands_path, "r") as commands_file:
        commands_data = json.load(commands_file)

    commands_dict = {}
    for command, description in commands_data.items():
        commands_dict[command] = description

    return commands_dict


def get_config():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_directory, "config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return config
