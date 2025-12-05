from .Record import Record


class ExpertRecord(Record):
    label: str

    def __init__(self):
        super().__init__()
        self.label = None