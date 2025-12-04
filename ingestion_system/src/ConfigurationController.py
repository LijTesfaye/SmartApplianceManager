import json


class ConfigurationController:
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_config = None

    def load_config(self):
        with open(self.file_path, 'r') as f:
            self.current_config = json.load(f)

    def get_ingestion_system_address(self):
        return self.current_config["ingestion_system"]

    def get_preparation_system_address(self):
        return self.current_config["preparation_system"]

    def get_evaluation_system_address(self):
        return self.current_config["evaluation_system"]

    def get_current_phase(self):
        return self.current_config["phase"]

    def get_minimum_records(self):
        return self.current_config["minimum_records"]

    def get_missing_samples_threshold(self):
        return self.current_config["missing_samples_threshold"]