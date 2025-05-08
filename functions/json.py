import json
import threading
import shutil

data_mappings = {
    "bot_location": {}
}

globals().update(data_mappings)

def save_data():
    total, used, free = shutil.disk_usage("/")
    if free < 1024 * 1024:
        print("Not enough disk space to save data.")
        return

    for var_name in data_mappings.keys():
        filename = f"functions/{var_name}.json"
        try:
            with open(filename, "w") as f:
                json.dump(globals()[var_name], f)
        except Exception as e:
            print(f"Error saving {filename}: {e}")

    threading.Timer(100, save_data).start()

def load_data():
    for var_name, default_value in data_mappings.items():
        filename = f"functions/{var_name}.json"
        try:
            with open(filename, "r") as f:
                globals()[var_name] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            globals()[var_name] = default_value

load_data()
save_data()
