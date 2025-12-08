""" Classification System main class"""

import json
from pathlib import Path
from threading import Thread
import jsonschema

from classifier.classifier import Classifier
from messaging.msg_json import MessagingJsonController
from model.prepared_session import PreparedSession
from errorlog.error_logger import ErrorLogger

class ClassificationSystem:
    """ Main system class """

    PHASE_PRODUCTION = "prod"
    PHASE_EVALUATION = "eval"

    def __init__(self):
        """ Constructor """
        self._system_config = None
        self._addresses = None
        self._msg_controller = None
        self._classifier = None
        self._session_counter = None
        self._current_session = None
        self._error_logger = None
        self._test_service_flag = True

    def import_cfg(self, file_name = "classification_system_config.json"):
        """ Import configuration file"""

        config_filepath = Path(__file__).parent.parent / "config" / file_name

        try:
            with open(config_filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self._system_config = config["system_parameters"]
                self._addresses = config["addresses"]
        except FileNotFoundError:
            print(f"Error: file {config_filepath} does not exist.")
        except json.JSONDecodeError:
            print(f"Error: file {config_filepath} is not in JSON format.")

    def setup_listener(self, ip, port):
        """ Setup listener thread """

        # Reference to msg_controller
        self._msg_controller = MessagingJsonController.get_instance()

        # Start listener on specified ip:port
        listener = Thread(target=self._msg_controller.listener, args=(ip, port))
        listener.setDaemon(True)
        listener.start()

    def setup_classifier(self):
        """ Setup classifier """
        # If not in development phase, setup classifier
        if not self._system_config["development_phase"]:
            self._classifier = Classifier()
            self._classifier.load_from_file()

    def setup_logger(self):
        """ Setup logger"""
        self._error_logger = ErrorLogger()
        self._error_logger.setup()

    def setup(self):
        """ Setup system """

        # Import configuration
        self.import_cfg()

        # Setup classifier
        self.setup_classifier()

        # Setup listener
        self.setup_listener(
            ip=self._addresses["classification_system"]["ip"],
            port=self._addresses["classification_system"]["port"],
        )

        # setup logger
        self.setup_logger()

        if not self._system_config["development_phase"]:
            self._session_counter = 0
            self._current_session = self.PHASE_EVALUATION
        else:
            self._session_counter = None

        print("[CLASSIFICATION SYSTEM] Setup completed")

    def update_phase(self):
        """ Updates the system current phase """

        # No automatic switch from dev phase
        if self._system_config["development_phase"]:
            return

        if self._session_counter is None:
            return

        # Update session counter
        self._session_counter += 1

        # Switch session
        if self._current_session == self.PHASE_PRODUCTION:
            if self._session_counter >= self._system_config["production_sessions"]:
                self._current_session = self.PHASE_EVALUATION
                self._session_counter = 0
                print("[CLASSIFICATION SYSTEM] Switched to evaluation phase")

        elif self._current_session == self.PHASE_EVALUATION:
            if self._session_counter >= self._system_config["evaluation_sessions"]:
                self._current_session = self.PHASE_PRODUCTION
                self._session_counter = 0
                print("[CLASSIFICATION SYSTEM] Switched to production phase")

    def run(self):
        """ Main loop """

        # Setup whole system
        self.setup()

        # Start loop
        while True:

            # Depending on which phase (dev or not)
            dev_phase = self._system_config["development_phase"]

            # While in development phase
            if dev_phase:

                try:
                    # Just wait for classifier
                    # in this case conversion is done by the msg module
                    classifier = self._msg_controller.receive()

                    print("[CLASSIFICATION SYSTEM] Classifier received")

                    # Save ref
                    self._classifier = classifier

                    # Save to file
                    self._classifier.store()

                    # Send message (end of development, reconfigure systems)
                    msg = {"deployment" : "done"}
                    MessagingJsonController.send_messaging_system(msg)

                    print("[CLASSIFICATION SYSTEM] Deployment completed")

                except Exception as e:
                    print(f"General error: {e}")
                    self._error_logger.log(f"General error: {e}")

            # Production / Evaluation phase
            else:

                # Wait for prepared session
                prepared_session_json = self._msg_controller.receive()

                try:
                    # Validate schema and create object
                    prep_session = PreparedSession.from_json(prepared_session_json)

                    print("[CLASSIFICATION SYSTEM] Prepared session received")

                    # Infer classifier
                    label = self._classifier.infer(prep_session)
                    print("[CLASSIFICATION SYSTEM] Label calculated")

                    # Differentiate between Production / Evaluation phase

                    if self._current_session == self.PHASE_EVALUATION:
                        # Send label
                        MessagingJsonController.send(
                            self._addresses["evaluation_system"]["ip"],
                            self._addresses["evaluation_system"]["port"],
                            "/label/classifier",
                            label.to_dict()
                        )

                    elif self._current_session == self.PHASE_PRODUCTION:
                        # Send message to final client
                        if not self._test_service_flag:
                            MessagingJsonController.send(
                                self._addresses["client_side_system"]["ip"],
                                self._addresses["client_side_system"]["port"],
                                "/fault_risk",
                                label.to_dict()
                            )
                        else:
                            print(f"(TEST) SENDING TO INGESTION:\n{label.to_dict()}")
                            ip = self._addresses["ingestion_system"]["ip"]
                            port = self._addresses["ingestion_system"]["port"]
                            print(f"TO [{ip}:{port}]")
                            MessagingJsonController.send(
                                self._addresses["ingestion_system"]["ip"],
                                self._addresses["ingestion_system"]["port"],
                                "/test_stop",
                                label.to_dict()
                            )

                    # Update session
                    self.update_phase()

                # Discard any other type of message
                except jsonschema.exceptions.ValidationError:
                    print("[CLASSIFICATION SYSTEM] [PROD/EVAL] Validation error")
                    self._error_logger.log(
                        f"[PROD/EVAL] json validation error: {prepared_session_json}")

                except Exception as e:
                    print(f"General error: {e}")
                    self._error_logger.log(f"General error: {e}")
