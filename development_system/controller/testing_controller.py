
from development_system.model.test_manager import TestManager

class TestController:
    def __init__(self):
      self._test_manager = TestManager()

    def evaluate_test_results(self):
        self._test_manager.evaluate_test_result()

    def generate_test_results(self):
        self._test_manager.generate_test_report()





