import json
import os
from typing import Callable

class BodyMetricsBackend:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._initialize_storage()

    def _initialize_storage(self):
        # Create the storage file if it doesn't already exist
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as file:
                json.dump([], file)

    def process_data(self, name: str, age: str, height: str, current_weight: str, goal_weight: str, sex: str):
        if not name or not age or not height or not current_weight or not goal_weight or not sex:
            return

        data = {
            "name": name,
            "age": int(age),
            "height": float(height),
            "current_weight": float(current_weight),
            "goal_weight": float(goal_weight),
            "sex": sex
        }

        self._save_to_storage(data)

    def _save_to_storage(self, data: dict):
        # Read existing data
        with open(self.storage_path, 'r') as file:
            existing_data = json.load(file)

        # Append new data
        existing_data.append(data)

        # Write updated data back to storage
        with open(self.storage_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

