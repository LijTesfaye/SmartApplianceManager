import warnings
import os
import pandas as pd
import joblib

from dotenv import load_dotenv
from pathlib import Path

from development_system.utility.json_read_write import JsonReadWrite
from development_system.model.smart_classifier_config import SMARTClassifierConfig

from sklearn.exceptions import ConvergenceWarning, DataConversionWarning
from sklearn.neural_network import MLPClassifier

# Ignore the Warnings
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", category=DataConversionWarning)


class SmartClassifier:
    def __init__(self):
        self._classifier = MLPClassifier()
        self._classifier_config = SMARTClassifierConfig()

        env_path = Path(__file__).resolve().parents[2] / "dev_sys.env"
        load_dotenv(env_path)
        config_path_from_root = os.getenv("HYPER_PARAMS_FILE_PATH")
        self.config_path = Path(__file__).resolve().parents[2] / config_path_from_root

        winner_joblib_path_from_root = os.getenv("WINNER_JOBLIB_PATH")
        self.winner_joblib_path = Path(__file__).resolve().parents[2] / winner_joblib_path_from_root

    def train_model(self, training_data, training_labels):
        training_data = pd.DataFrame(training_data)
        self._classifier.fit(training_data, training_labels)

    def update_classifier_config(self, new_config: SMARTClassifierConfig):
        """
        Update internal config and, if needed, update the JSON config file and
        reconfigure the underlying classifier.
        """
        previous_config = self._classifier_config

        iterations_changed = (previous_config is not None
                              and previous_config.num_iterations != new_config.num_iterations
                              )

        if previous_config is None or iterations_changed:
            print("[DEBUG] Update SMART classifier config file")
            JsonReadWrite.update_json_file(
                self.config_path,
                "num_iterations",
                new_config.num_iterations
            )
        self._classifier_config = new_config
        self._classifier.set_params(**new_config.to_dict())

    def get_error(self, data, labels):
        data = pd.DataFrame(data)
        return self._classifier.score(data, labels)

    def grab_training_losses(self):
        return self._classifier.loss_curve_

    # Saves a WinnerClassifier to the CANDIDATE_CLASSIFIERS_DIRECTORY_PATH
    def save_classifier(self, uuid):
        file_path = Path(self.winner_joblib_path) / f"{uuid}.joblib"
        joblib.dump(self._classifier, file_path)

    # used in the test phase, takes the winner classifier from the  CANDIDATE_CLASSIFIERS_DIRECTORY_PATH to WINNER_CLASSIFIER_DIRECTORY_PATH
    def load_classifier(self, uuid):
        file_path = Path(self.winner_joblib_path) / f"{uuid}.joblib"
        self._classifier = joblib.load(file_path)
