import os
from dotenv import load_dotenv
from pathlib import Path
from development_system.utility.json_read_write import JsonReadWrite


class DevSystemConfig:
    def __init__(self):
        env_path = Path(__file__).resolve().parents[2] / "dev_sys.env"
        load_dotenv(env_path)
        config_path_from_root = os.getenv("DEV_SYSTEM_CONFIG")
        self.config_path = Path(__file__).resolve().parents[2] / config_path_from_root

        read_result, file_content = JsonReadWrite.read_json_file(self.config_path)

        print(file_content)
        print(read_result)
        if not read_result:
            return
        self.startup_mode = file_content["startup_mode"]
        self.stage = file_content["stage"]
        self.ongoing_validation = file_content["ongoing_validation"]

    def update_stage(self):
        JsonReadWrite.update_json_file(self.config_path, "stage", self.stage)
