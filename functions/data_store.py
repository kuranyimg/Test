import json
import os

DATA_FILE = "functions/data.json"

default_data = {
    "mods": ["RayBM"],
    "vips": [],
    "floors": {
        "1": None,
        "2": None,
        "3": None
    }
}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(default_data, f, indent=4)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_mod(username):
    data = load_data()
    if username not in data["mods"]:
        data["mods"].append(username)
        save_data(data)

def is_mod(username):
    data = load_data()
    return username in data["mods"] or username == "RayBM"

def add_vip(username):
    data = load_data()
    if username not in data["vips"]:
        data["vips"].append(username)
        save_data(data)

def is_vip(username):
    data = load_data()
    return username in data["vips"]

def save_floor(number, pos):
    data = load_data()
    data["floors"][str(number)] = {"x": pos.x, "y": pos.y, "z": pos.z, "facing": pos.facing}
    save_data(data)

def get_floor(number):
    data = load_data()
    return data["floors"].get(str(number))
