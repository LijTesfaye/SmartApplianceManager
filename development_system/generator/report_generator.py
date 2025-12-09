import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict
import plotly.graph_objects as go

from development_system.utility.json_read_write import JsonReadWrite

@dataclass
class ReportGenerator:
    """Report generator.
    This class generates a report for the given report type: i.e "training", "validation", or "test"
    """
    report_type: str  # very important to identify who calls this class.

    learning_losses: Optional[List[float]] = None     # gonna be used for the training report
    best_classifiers: Optional[list] = None           # used by the validation report
    test_result: Optional[Dict] = None                # needed to do  test report


    def __post_init__(self):
        if self.report_type not in ("training", "validation", "test"):
            raise ValueError(f"Invalid report_type: {self.report_type}")

        env_path = Path(__file__).resolve().parents[2] / "dev_sys.env"
        load_dotenv(env_path)

        test_report_path_from_root = os.getenv("TEST_REPORT_PATH")
        self.test_report_path = Path(__file__).resolve().parents[2] / test_report_path_from_root

        validation_report_path_from_root = os.getenv("VALIDATION_TEST_REPORT_PATH")
        self.validation_report_path = Path(__file__).resolve().parents[2] / validation_report_path_from_root

        test_image_path_from_root = os.getenv("TEST_IMAGE_DIR")
        self.test_image_path = Path(__file__).resolve().parents[2] / test_image_path_from_root

    def generate_report(self) -> None:
        if self.report_type == "training":
            self._generate_training_report()
        elif self.report_type == "validation":
            self._generate_validation_report()
        elif self.report_type == "test":
            self._generate_test_report()
        else:
            raise ValueError(f"Unknown report type: {self.report_type!r}")

    def _generate_training_report(self) -> None:
        # Learning curve
        if not self.learning_losses:
            raise ValueError("Training report cannot be generated — learning_losses is missing.")
        self._learning_plot()

    def _generate_validation_report(self):
        if not self.best_classifiers:
            raise ValueError("Validation report requires best_classifiers")
        path = self.validation_report_path
        if not path:
            raise ValueError("VALIDATION_JSON_PATH is not set in the environment.")
        self._generate_json(self.best_classifiers, path)

    def _generate_test_report(self):
        if not self.test_result:
            raise ValueError("Test report requires test_result value")

        data = [self.test_result]
        json_path = self.validation_report_path
        if json_path is not None:
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            self._generate_json(data, json_path)

    def _generate_json(self, data, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        JsonReadWrite.write_json_file(str(file_path), data)

    def _learning_plot(self) -> None:
        fig = go.Figure(layout_title_text="MSE chart for classifier error")
        fig.add_trace(
            go.Scatter(
                y=self.learning_losses,
                mode="lines+markers",
                name="error",
                showlegend=True,
            )
        )
        fig.write_image(self.test_image_path)
        print(f"[INFO] Learning plot saved at: {self.test_image_path}")
