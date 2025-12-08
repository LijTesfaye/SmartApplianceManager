""" Module for defining the classifier """
import io
import os
import joblib

from production_system.model.label import Label
from production_system.model.label_type import LabelType
from production_system.model.prepared_session import PreparedSession


class Classifier:
    """ Class for managing the classifier """


    def __init__(self):
        self.filename = None
        self.model = None

    def load_from_file(self, filename: str = "classifier.joblib"):
        """ Loads the classifier from a file """
        self.filename = filename

        # TODO
        #  uncomment.
        #  Tieni salvato un modello random, anche solo per test
        # self.model = joblib.load(filename)

    def load_from_bytes(self, raw_bytes: bytes):
        """ Loads the classifier from bytes """
        self.model = joblib.load(io.BytesIO(raw_bytes))

    def store(self, filename: str = "classifier.joblib"):
        """Store current model into a .joblib file inside the working directory."""

        if self.model is None:
            print("ERROR No model loaded, cannot store.")
            return

        working_dir = os.getcwd()
        full_path = os.path.join(working_dir, filename)

        joblib.dump(self.model, full_path)

        self.filename = full_path


    def infer(self, prepared_session):
        """Run inference."""
        # TODO delete
        #  metti la prediciton vera
        return Label(
            uuid = prepared_session.get_uuid(),
            label_type = LabelType.from_string("none")
        )

        if self.model is None:
            raise RuntimeError("Classifier model not loaded")

        features = prepared_session.to_tuple()
        pred = self.model.predict([features])[0]

        return Label(
            uuid=prepared_session.get_uuid(),
            label_type=LabelType.from_string(str(pred))
        )
