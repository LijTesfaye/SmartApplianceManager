""" Module for defining label pairs """

from model.label import Label
from model.label_source import LabelSource

class LabelPair:
    """ Class for managing label pairs """

    def __init__(self, UUID, label_expert: Label, label_classifier: Label):
        self._UUID = UUID
        self._label_expert = label_expert.get_label_type()
        self._label_classifier = label_classifier.get_label_type()

    def get_UUID(self):
        """ Get the UUID """
        return self._UUID

    def get_label_expert(self) -> LabelSource:
        """ Get the label expert """
        return self._label_expert

    def get_label_classifier(self) -> LabelSource:
        """ Get the label classifier """
        return self._label_classifier

    def are_label_different(self):
        """ Check if two label pairs are different """
        return self._label_expert.value != self._label_classifier.value
