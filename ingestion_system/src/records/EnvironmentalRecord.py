from .Record import Record


class EnvironmentalRecord(Record):
    temperature: float
    humidity: float

    def __init__(self):
        super().__init__()
        self.temperature = None
        self.humidity = None