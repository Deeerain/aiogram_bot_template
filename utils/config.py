import json

def get_config():
    with open("config.json", "r") as file:
        return json.load(file)