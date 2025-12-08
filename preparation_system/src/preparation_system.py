import json
import sys
import logging
from threading import Thread
from preparation_system.src.json_io import JsonIO
from preparation_system.src.cleaner import Cleaner
from preparation_system.src.extractor import Extractor
from preparation_system.src.raw_session_schema_verifier import RawSessionSchemaVerifier
from preparation_system.src.preparation_system_configurator import PreparationSystemConfigurator

LOG_FILE = "preparation_system.log"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class PreparationSystem:

    def __init__(self):
        self.preparation_system_config = None
        self.raw_session_schema_verifier = RawSessionSchemaVerifier()
        self.preparation_system_configurator = PreparationSystemConfigurator()

    def run(self):
        self.preparation_system_config = self.preparation_system_configurator.import_cfg()

        logging.info("Configuration loaded")

        jsonIO = JsonIO.get_instance()
        listener = Thread(
            target=jsonIO.listener,
            args=(self.preparation_system_config["preparation_system"]["ip"],
                  self.preparation_system_config["preparation_system"]["port"])
        )
        listener.setDaemon(True)
        listener.start()

        while True:

            raw_session = JsonIO.get_instance().receive()
            logging.info("Raw session received")

            if not self.raw_session_schema_verifier.verify(raw_session):
                logging.error("Raw session received is invalid")
                continue

            cleaner = Cleaner(self.preparation_system_config["limits"])

            raw_session = cleaner.correct_missing_samples(raw_session)
            logging.info("Missing samples corrected")

            raw_session = cleaner.correct_outliers(raw_session)
            logging.info("Outliers corrected")

            extractor = Extractor(raw_session)
            prepared_session = extractor.extract()
            logging.info("Prepared session extracted")

            is_development_phase = bool(self.preparation_system_config['development_phase'])

            next_system = 'production_system'
            if is_development_phase:
                next_system = 'segregation_system'

            logging.info("Prepared session ready")
            logging.info(prepared_session)

            JsonIO.get_instance().send(
                self.preparation_system_config[next_system]["ip"],
                self.preparation_system_config[next_system]["port"],
                "/prepared_session",
                prepared_session
            )

            logging.info("Prepared session sent")
