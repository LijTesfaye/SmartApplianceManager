""" Classification System main class"""

from threading import Thread
import jsonschema

from config.configuration_controller import ConfigurationController
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
        self._conf = None
        self._msg_controller = None
        self._classifier = None
        self._session_counter = None
        self._current_session = None
        self._error_logger = None
        self._test_service_flag = True

    def setup_configuration_controller(self):
        """ Setup configuration controller """
        self._conf = ConfigurationController()
        self._conf.import_config()

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
        if not self._conf.get_sys_params()["development_phase"]:
            self._classifier = Classifier()
            self._classifier.load_from_file()

    def setup_logger(self):
        """ Setup logger"""
        self._error_logger = ErrorLogger()
        self._error_logger.setup()

    def setup(self):
        """ Setup system """

        # Import configuration
        self.setup_configuration_controller()

        # Setup classifier
        self.setup_classifier()

        # Setup listener
        self.setup_listener(
            ip=self._conf.get_addresses()["classification_system"]["ip"],
            port=self._conf.get_addresses()["classification_system"]["port"],
        )

        # setup logger
        self.setup_logger()

        if not self._conf.get_sys_params()["development_phase"]:
            self._session_counter = 0
            self._current_session = self.PHASE_EVALUATION
        else:
            self._session_counter = None

        print("[CLASSIFICATION SYSTEM] Setup completed")

    def update_phase(self):
        """ Updates the system current phase """

        # No automatic switch from dev phase
        if self._conf.get_sys_params()["development_phase"]:
            return

        if self._session_counter is None:
            return

        # Update session counter
        self._session_counter += 1

        # Switch session
        if self._current_session == self.PHASE_PRODUCTION:
            if self._session_counter >= self._conf.get_sys_params()["production_sessions"]:
                self._current_session = self.PHASE_EVALUATION
                self._session_counter = 0
                print("[CLASSIFICATION SYSTEM] Switched to evaluation phase")

        elif self._current_session == self.PHASE_EVALUATION:
            if self._session_counter >= self._conf.get_sys_params()["evaluation_sessions"]:
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
            dev_phase = self._conf.get_sys_params()["development_phase"]

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

                    msg = {"deployment": "done"}
                    if not self._test_service_flag:
                        MessagingJsonController.send_messaging_system(msg)
                    else:
                        print("(TEST) SENDING classifier TO INGESTION")
                        ip = self._conf.get_addresses()["ingestion_system"]["ip"]
                        port = self._conf.get_addresses()["ingestion_system"]["port"]
                        print(f"TO [{ip}:{port}]")
                        MessagingJsonController.send(
                            self._conf.get_addresses()["ingestion_system"]["ip"],
                            self._conf.get_addresses()["ingestion_system"]["port"],
                            "/test_stop",
                            msg
                        )


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

                    # In evaluation phase send label to Evaluation System
                    if self._current_session == self.PHASE_EVALUATION:
                        # Send label
                        MessagingJsonController.send(
                            self._conf.get_addresses()["evaluation_system"]["ip"],
                            self._conf.get_addresses()["evaluation_system"]["port"],
                            "/label/classifier",
                            label.to_dict()
                        )

                    # Always send to final client
                    if not self._test_service_flag:
                        MessagingJsonController.send(
                            self._conf.get_addresses()["client_side_system"]["ip"],
                            self._conf.get_addresses()["client_side_system"]["port"],
                            "/fault_risk",
                            label.to_dict()
                        )
                    else:
                        print(f"(TEST) SENDING TO INGESTION:\n{label.to_dict()}")
                        ip = self._conf.get_addresses()["ingestion_system"]["ip"]
                        port = self._conf.get_addresses()["ingestion_system"]["port"]
                        print(f"TO [{ip}:{port}]")
                        MessagingJsonController.send(
                            self._conf.get_addresses()["ingestion_system"]["ip"],
                            self._conf.get_addresses()["ingestion_system"]["port"],
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
