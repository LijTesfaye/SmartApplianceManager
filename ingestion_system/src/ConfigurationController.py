import json


class ConfigurationController:
    """
    Provides the values contained in the configuration file
    """

    file_path: str
    """
    Path to the configuration file
    """

    current_config: dict
    """
    Json object of the configuration file
    """

    def __init__(self, file_path: str):
        """
        Constructor, it will read the specified configuration file
        :param file_path: str
        """

        self.file_path = file_path
        self.current_config = None

    def load_config(self):
        """
        Loads the configuration file
        :return: None
        """
        with open(self.file_path, 'r') as f:
            self.current_config = json.load(f)

    def get_ingestion_system_address(self) -> dict:
        """
        Gets the ingestion system address (ip and port)
        :return: dict
        """
        return self.current_config["ingestion_system"]

    def get_preparation_system_address(self) -> dict:
        """
        Gets the preparation system address (ip and port)
        :return: dict
        """
        return self.current_config["preparation_system"]

    def get_evaluation_system_address(self) -> dict:
        """
        Gets the evaluation system address (ip and port)
        :return: dict
        """
        return self.current_config["evaluation_system"]

    def get_current_phase(self) -> str:
        """
        Gets the current phase
        :return: str
        """
        return self.current_config["currentPhase"]

    def get_minimum_records(self) -> int:
        """
        Gets the minimum number of records to constitute a raw session
        :return: int
        """
        return self.current_config["minimumRecords"]

    def get_missing_samples_threshold(self) -> int:
        """
        Gets the number of samples missing from the raw session
        :return: int
        """
        return self.current_config["missingSamplesThreshold"]

    def get_records_collection_period_seconds(self) -> int:
        """
        Cooldown for the records collection period in seconds
        :return: int
        """
        return self.current_config["recordsCollectionPeriodSeconds"]

    def get_preparation_system_endpoint(self) -> str:
        """
        Gets the preparation system endpoint
        :return: str
        """
        return self.current_config["preparationSystemEndpoint"]

    def get_evaluation_system_endpoint(self) -> str:
        """
        Gets the evaluation system endpoint
        :return: str
        """
        return self.current_config["evaluationSystemEndpoint"]