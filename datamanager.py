import json


class DataManager:
    @staticmethod
    def load_data(filename, transform=None):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return [transform(item) for item in data] if transform else data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_data(filename, data):
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data to {filename}: {e}")
