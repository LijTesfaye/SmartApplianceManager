""" Module for defining the configuration controller """
import json
from pathlib import Path

class ConfigurationController:
    """ Class for handling the system configuration """
    def __init__(self):
        self._addresses = None
        self._sys_params = None

    def import_config(self, filename = "classification_system_config.json"):
        """ Import configuration file"""

        config_filepath = Path(__file__).parent / filename

        try:
            with open(config_filepath, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                self._addresses = cfg['addresses']
                self._sys_params = cfg['system_parameters']
        except FileNotFoundError:
            print(f"Error: file {config_filepath} does not exist.")
        except json.JSONDecodeError:
            print(f"Error: file {config_filepath} is not in JSON format.")

    def get_addresses(self):
        """ Get addresses """
        return self._addresses

    def get_sys_params(self):
        """ Get system parameters """
        return self._sys_params
