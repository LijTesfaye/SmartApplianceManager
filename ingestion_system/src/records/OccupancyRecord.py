from .Record import Record


class OccupancyRecord(Record):
    occupancy: int

    def __init__(self):
        super().__init__()
        self.occupancy = None