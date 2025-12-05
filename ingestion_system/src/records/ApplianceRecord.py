from .Record import Record


class ApplianceRecord(Record):
    current: float
    voltage: float
    temperature: float
    appliance_type: str

    def __init__(self):
        super().__init__()
        self.current = None
        self.voltage = None
        self.temperature = None
        self.appliance_type = None