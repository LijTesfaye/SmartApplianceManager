""" Module for defining the error logger """
import os
from datetime import datetime

class ErrorLogger:
    """ Class for handling the error logger """

    def __init__(self):
        self._log_filepath = None

    def setup(self, log_filename="log.txt"):
        """Creates the log file if it doesn't exist and writes a session header."""
        log_dir = os.path.abspath("errorlog")
        os.makedirs(log_dir, exist_ok=True)
        self._log_filepath = os.path.join(log_dir, log_filename)

        with open(self._log_filepath, "a", encoding="utf-8") as f:
            f.write("\n\n======================\nNEW WORKING SESSION\n")

    def log(self, text):
        """Appends a log line with timestamp."""
        if not self._log_filepath:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self._log_filepath, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")
