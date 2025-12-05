from ingestion_system.src.records.ApplianceRecord import ApplianceRecord
from ingestion_system.src.records.EnvironmentalRecord import EnvironmentalRecord
from ingestion_system.src.records.ExpertRecord import ExpertRecord
from ingestion_system.src.records.OccupancyRecord import OccupancyRecord


class RawSession:
    uuid: int
    appliance_records: list[ApplianceRecord]
    environmental_records: list[EnvironmentalRecord]
    occupancy_records: list[OccupancyRecord]
    expert_record: ExpertRecord

    def __init__(self):
        self.uuid = None
        self.appliance_records = None
        self.environmental_records = None
        self.occupancy_records = None
        self.expert_record = None