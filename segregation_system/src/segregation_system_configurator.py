import json
from pathlib import Path


class SegregationSystemConfigurator:

    def __init__(self):
        self.file_path = Path(__file__).parent.parent / "segregation_system_config.json"

    def import_cfg(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"File {self.file_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError(f"File {self.file_path} is not valid JSON.")