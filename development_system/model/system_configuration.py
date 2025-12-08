import os

from development_system.utility.json_read_write import JsonReadWrite

class  DevSystemConfig:
    def __init__(self):
        read_result, file_content = JsonReadWrite.read_json_file(os.getenv("DEV_SYSTEM_CONFIG"))
        if not read_result:
            return
        self.startup_mode = file_content["startup_mode"]
        self.stage = file_content["stage"]
        self.ongoing_validation = file_content["ongoing_validation"]

    def update_stage(self):
        JsonReadWrite.update_json_file(os.getenv("DEV_SYSTEM_CONFIG") , "stage" , self.stage)

