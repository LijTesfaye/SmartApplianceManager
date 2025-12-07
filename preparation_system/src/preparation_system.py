import json
from pathlib import Path
from threading import Thread
from preparation_system.src.json_io import JsonIO
from preparation_system.src.cleaner import Cleaner
from preparation_system.src.extractor import Extractor
from preparation_system.src.raw_session_schema_verifier import RawSessionSchemaVerifier


class PreparationSystem:

    def __init__(self):
        self.preparation_system_config = None
        self.raw_session_schema_verifier = RawSessionSchemaVerifier()

    def import_cfg(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self.preparation_system_config = json.load(f)
        except FileNotFoundError:
            print(f"Error: file {file_path} does not exist.")
        except json.JSONDecodeError:
            print(f"Error: file {file_path} is not in JSON format.")

    def run(self):
        file_path = Path(__file__).parent.parent / "preparation_system_config.json"
        self.import_cfg(file_path)

        if self.preparation_system_config is None:
            raise ValueError("Configuration not imported. Call import_cfg(file_path) first.")

        print(f"[PREPARATION SYSTEM] Configuration loaded")

        jsonIO = JsonIO.get_instance()
        listener = Thread(target=jsonIO.listener,
                          args=(self.preparation_system_config["preparation_system"]["ip"],
                                self.preparation_system_config["preparation_system"]["port"]))
        listener.setDaemon(True)
        listener.start()

        while True:

            raw_session = JsonIO.get_instance().receive()
            print("[PREPARATION SYSTEM] Raw session received.")

            if not self.raw_session_schema_verifier.verify(raw_session):
                print("[PREPARATION SYSTEM] Raw session received is invalid.")

            cleaner = Cleaner(self.preparation_system_config["limits"])

            raw_session = cleaner.correct_missing_samples(raw_session)
            print("[PREPARATION SYSTEM] Raw session missing samples corrected.")

            raw_session = cleaner.correct_outliers(raw_session)
            print("[PREPARATION SYSTEM] Raw session outliers corrected.")

            extractor = Extractor(raw_session)
            prepared_session = extractor.extract()
            print("[PREPARATION SYSTEM] Prepared session extracted from raw session.")

            is_development_phase = bool(self.preparation_system_config['development_phase'])

            next_system = 'production_system'
            if is_development_phase:
                next_system = 'segregation_system'

            print("[PREPARATION SYSTEM] Prepared")
            print(prepared_session)

            JsonIO.get_instance().send(self.preparation_system_config[next_system]["ip"],
                                       self.preparation_system_config[next_system]["port"],
                                       "/prepared_session",
                                       prepared_session)
