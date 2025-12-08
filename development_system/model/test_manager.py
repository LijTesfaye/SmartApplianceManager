import os

from development_system.generator.report_generator import ReportGenerator
from development_system.model.learning_set_data import LearningDataSet
from development_system.model.smart_classifier import SmartClassifier
from development_system.utility.json_read_write import JsonReadWrite


class TestManager:

    def __init__(self):
        self._smart_classifier = SmartClassifier()
        self._validation_data = LearningDataSet.get_data("validation")
        self._test_data = LearningDataSet.get_data("test")

        base_dir = os.getenv("JSON_PATH")
        file_name ="winner_classifier.json"
        winner_json_path = os.path.join(base_dir, file_name)
        read_result, file_content = JsonReadWrite.read_json_file(winner_json_path)
        if not read_result:
            print("[ERROR] No winner_classifier file found")
            return
        self._winner_uuid = file_content["uuid"]


        self._result = {}

    def _load_data(self):
            if self._validation_data is None or self._test_data is None:
                self._validation_data = LearningDataSet.get_data("validation")
                self._test_data = LearningDataSet.get_data("test")


    # We do the test on the winner classifier
    def evaluate_test_result(self):
        #self._load_data()
        self._smart_classifier.load_classifier(self._winner_uuid)
        validation_error = self._smart_classifier.get_error(self._validation_data["data"],
                                                             self._validation_data["labels"])

        test_error = self._smart_classifier.get_error(self._test_data["data"],
                                                       self._test_data["labels"])

        self._result = {
            "uuid": self._winner_uuid,
            "test_error": test_error,
            "validation_error": validation_error,
            "difference": abs(test_error - validation_error)
        }

    # Generated the test report on winner classifier.
    def generate_test_report(self):
        read_result, file_content = JsonReadWrite.read_json_file(os.getenv("HYPER_PARAMS_FILE_PATH"))
        if not read_result:
            return
        self._result["generalization_tolerance"] = file_content["generalization_tolerance"]
        test_report_generator = ReportGenerator(report_type="test",
                                                test_result=self._result)
        test_report_generator.generate_report()
