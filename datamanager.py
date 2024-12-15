import json

""" 
Class that handles the saving and loading of data to/from a file. 
It helps store and retrieve information such as customer details, bike rentals, etc.
We use JSON format for saving, which makes it easy to read and store data in files.
"""

class DataManager:

    # Static method to load data from a file and optionally transform each item
    @staticmethod
    def load_data(filename, transform=None):
        try:
            # Open the file in read mode and load the data into a Python object
            with open(filename, "r") as file:
                data = json.load(file)  # Load JSON data into Python objects
                return [transform(item) for item in data] if transform else data
        except (FileNotFoundError, json.JSONDecodeError):
            # Returns an empty list if the file is not found or the data is invalid
            return []
            
    # Static method to save data to a file
    @staticmethod
    def save_data(filename, data):
        try:
            # Opens the file in write mode and the data to the file in JSON format
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)  # Write the data to a file as JSON
        except Exception as e: 
            print(f"Error saving data to {filename}: {e}")
