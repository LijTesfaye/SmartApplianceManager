from ingestion_system.src.records.ApplianceRecord import ApplianceRecord
from ingestion_system.src.records.EnvironmentalRecord import EnvironmentalRecord
from ingestion_system.src.records.ExpertRecord import ExpertRecord
from ingestion_system.src.records.OccupancyRecord import OccupancyRecord


class RawSession:
    """
    Raw session containing the buffered records
    """

    uuid: int
    """
    unique identifier
    """

    appliance_records: list[ApplianceRecord]
    """
    appliance records gathered
    """

    environmental_records: list[EnvironmentalRecord]
    """
    environmental records gathered
    """

    occupancy_records: list[OccupancyRecord]
    """
    occupancy records gathered
    """

    expert_record: ExpertRecord
    """
    label associated to the records, it is different from None only if we are in the evaluation and development phase
    """

    def __init__(self):
        """
        Constructor
        """
        self.uuid = None
        self.appliance_records = None
        self.environmental_records = None
        self.occupancy_records = None
        self.expert_record = None

    def to_dict(self) -> dict:
        """
        Converts the raw session into a dictionary
        :return: dict
        """
        ret = {
            "UUID": self.uuid,
            "applianceRecords": [],
            "environmentalRecords": [],
            "occupancyRecords": [],
            "expertRecord": self.expert_record.to_dict()
        }

        for record in self.appliance_records:
            ret["applianceRecords"].append(record.to_dict())
        for record in self.environmental_records:
            ret["environmentalRecords"].append(record.to_dict())
        for record in self.occupancy_records:
            ret["occupancyRecords"].append(record.to_dict())

        return ret