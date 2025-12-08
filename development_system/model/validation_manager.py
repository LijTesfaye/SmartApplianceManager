import math
import os
from itertools import product
from operator import itemgetter

from dotenv import load_dotenv
from pathlib import Path

import shutil

from development_system.generator.report_generator import ReportGenerator
from development_system.model.learning_set_data import LearningDataSet
from development_system.model.smart_classifier import SmartClassifier
from development_system.model.smart_classifier_config import SMARTClassifierConfig
from development_system.utility.json_read_write import JsonReadWrite


class ValidationManager:
    def __init__(self):
        self._smart_classifier = SmartClassifier()
        self._train_data = LearningDataSet.get_data("training")
        self._validation_data = LearningDataSet.get_data("validation")
        self._candidate_classifiers = []

        env_path = Path(__file__).resolve().parents[2] / "dev_sys.env"
        load_dotenv(env_path)
        config_path_from_root = os.getenv("HYPER_PARAMS_FILE_PATH")
        self.config_path = Path(__file__).resolve().parents[2] / config_path_from_root

        top5_classifiers_from_root = os.getenv("TOP5_CLASSIFIER_PATH")
        self.top5_classifiers_path = Path(__file__).resolve().parents[2] / top5_classifiers_from_root

        winner_from_root = os.getenv("WINNER_PATH")
        self.winner_path = Path(__file__).resolve().parents[2] / winner_from_root

        winner_joblib_from_root = os.getenv("WINNER_JOBLIB_PATH")
        self.winner_joblib_path = Path(__file__).resolve().parents[2] / winner_joblib_from_root

    def generate_hyperparameter_options(self):
        read_result, file_content = JsonReadWrite.read_json_file(self.config_path)
        if not read_result:
            print("No HYPER_PARAMS_FILE_PATH file found")
            return [], None, None

        num_iterations = file_content["num_iterations"]
        overfitting_threshold = file_content["overfitting_tolerance"]
        hidden_layer_size_range = file_content["hidden_layer_range"]
        hidden_neuron_range = file_content["neuron_range"]

        max_exp = int(math.log2(hidden_neuron_range[1]))  # 128 -> 7
        min_exp = int(math.log2(hidden_neuron_range[0]))  # 4   -> 2
        neuron_options = [2 ** i for i in range(max_exp, min_exp - 1, -1)]

        hidden_layer_sizes_options = []

        for n_layers in range(hidden_layer_size_range[0], hidden_layer_size_range[1] + 1):
            # use all possible tuples
            layer_combinations = list(product(neuron_options, repeat=n_layers))
            for combination in layer_combinations:
                is_decreasing = all(
                    combination[i] >= combination[i + 1] for i in range(len(combination) - 1)
                )
                if is_decreasing:
                    hidden_layer_sizes_options.append(combination)
        return hidden_layer_sizes_options, num_iterations, overfitting_threshold

    def get_candidate_classifiers(self):

        grid_search_result, iterations_number, overfitting_threshold = self.generate_hyperparameter_options()

        if not grid_search_result:
            print("[WARN] No hyperparameter settings generated, skipping validation.")
            return

        for index, setting in enumerate(grid_search_result):
            new_config = SMARTClassifierConfig(iterations_number, setting)

            self._smart_classifier.update_classifier_config(new_config)

            self._smart_classifier.train_model(self._train_data["data"], self._train_data["labels"])

            train_error = self._smart_classifier.get_error(
                self._train_data["data"],
                self._train_data["labels"]
            )

            validation_error = self._smart_classifier.get_error(
                self._validation_data["data"],
                self._validation_data["labels"]
            )

            if (validation_error - train_error) > overfitting_threshold:
                continue

            self._smart_classifier.save_classifier("NN" + str(index))

            neurons = sum(setting)

            model = {
                "uuid": "NN" + str(index),
                "train_error": train_error,
                "validation_error": validation_error,
                "layers": len(setting),
                "neurons": neurons,
                "hidden_layers_structure": setting,
                "error_difference": abs(validation_error - train_error),
                "overfitting_threshold": overfitting_threshold
            }

            self._candidate_classifiers.append(model)
            self._candidate_classifiers = sorted(
                self._candidate_classifiers,
                key=itemgetter('validation_error')
            )

            # A check that the top classifiers selected are not more than FIVE
            if len(self._candidate_classifiers) > 5:
                self._candidate_classifiers.pop(5)

        # The top-5  candidate classifiers are saved into JSON here
        self.save_top5_classifiers_json()
        print("[DEBUG] THE BEST 5 CLASSIFIERS  : ", self._candidate_classifiers)

    def save_top5_classifiers_json(self):
        JsonReadWrite.write_json_file(self.top5_classifiers_path, self._candidate_classifiers)
        print(f"[INFO] Saved top 5 classifier metadata at {self.top5_classifiers_path}")

    def winner_classifier(self, uuid):
        # Read the top5 classifiers JSON
        read_result, file_content = JsonReadWrite.read_json_file(self.top5_classifiers_path)
        if not read_result:
            print("[ERROR] winner_classifier not found")
            return

        # Locate the selected winner
        winner = next((clf for clf in file_content if clf["uuid"] == uuid), None)
        if not winner:
            print(f"[WARN] No classifier with UUID {uuid} found in top5_classifiers.json")
            return

        JsonReadWrite.write_json_file(self.winner_path, winner)
        print(f"[INFO] Winner classifier metadata saved at {self.winner_path}")

        # Clean up the candidate directory (keep only the winner joblib)
        self.classifier_dir_archiver(uuid)

    def classifier_dir_archiver(self, uuid):
        winner_file = uuid + ".joblib"
        for filename in os.listdir(self.winner_joblib_path):
            file_path = os.path.join(self.winner_joblib_path, filename)
            if filename == winner_file:
                continue
            if not filename.endswith(".joblib"):
                continue
            if os.path.isfile(file_path):
                os.remove(file_path)

    def generate_validation_result(self):
        self.save_top5_classifiers_json()
        report_generator = ReportGenerator(report_type="validation",
                                           best_classifiers=self._candidate_classifiers)
        report_generator.generate_report()
