import json
from pathlib import Path


class PreparationSystemConfigurator:

    def __init__(self):
        file_path = Path(__file__).parent.parent / "preparation_system_config.json"

    def import_cfg(self):
        file_path = Path(__file__).parent.parent / "preparation_system_config.json"
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"File {file_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError(f"File {file_path} is not valid JSON.")