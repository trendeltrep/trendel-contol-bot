import json
import loading

file_name = "statics.json"


def load():
    try:
        with open(file_name, "r") as file:
            commands = loading.get_commands()
            return json.load(file)
    except FileNotFoundError:
        with open(file_name, "w") as file:
            data = loading.get_commands()
            data_used = {used: 0 for used in data}
            json.dump(data_used, file)
            return data_used


try:
    data = load()
except:
    pass


# Saving data to statics.json
def save_data():
    with open(file_name, "w") as file:
        json.dump(data, file)


# Resetting data to default
def reset_data():
    with open(file_name, "w") as file:
        data = loading.get_commands()
        data_used = {used: 0 for used in data}
        json.dump(data_used, file)
