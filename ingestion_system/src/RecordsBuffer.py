import sqlite3

from ingestion_system.src.records.ApplianceRecord import ApplianceRecord
from ingestion_system.src.records.EnvironmentalRecord import EnvironmentalRecord
from ingestion_system.src.records.OccupancyRecord import OccupancyRecord
from ingestion_system.src.records.Record import Record


class RecordsBuffer:
    """
    RecordsBuffer will provide necessary apis between the orchestrator and the records database
    """

    db_name: str
    """
    The name of the database file
    """

    stored_records: int
    """
    Number of stored records
    """

    def __init__(self):
        """
        Constructor
        """
        self.db_name = "recordsBuffer.db"
        self.stored_records = -1
        conn = sqlite3.connect(self.db_name)

        # init database
        cursor = conn.cursor()

        # appliance record table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ApplianceRecord (
            uuid INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            current FLOAT,
            voltage FLOAT,
            temperature FLOAT,
            applianceType TEXT
        )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EnvironmentalRecord (
                uuid INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                temperature FLOAT,
                humidity FLOAT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OccupancyRecord (
                uuid INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                occupancy INTEGER
            )
        """)
        conn.commit()
        conn.close()
        self.stored_records = self.get_records_count()

    def store_record(self, record: Record):
        """
        Stores the specified record in the database
        :param record: Record
        :return: None
        """
        if isinstance(record, ApplianceRecord):
            self.store_appliance(record)
        elif isinstance(record, EnvironmentalRecord):
            self.store_environmental(record)
        elif isinstance(record, OccupancyRecord):
            self.store_occupancy(record)
        self.stored_records += 1


    def store_appliance(self, record: ApplianceRecord):
        """
        Stores the appliance record in the database
        :param record: ApplianceRecord
        :return: None
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
        "INSERT INTO ApplianceRecord (timestamp, current, voltage, temperature, applianceType) VALUES (?, ?, ?, ?, ?)",
    (record.timestamp, record.current, record.voltage, record.temperature, record.appliance_type)
        )
        conn.commit()
        conn.close()

    def store_environmental(self, record: EnvironmentalRecord):
        """
        Stores the environmental record in the database
        :param record: EnvironmentalRecord
        :return: None
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO EnvironmentalRecord (timestamp, temperature, humidity) VALUES (?, ?, ?)",
            (record.timestamp, record.temperature, record.humidity)
        )
        conn.commit()
        conn.close()

    def store_occupancy(self, record: OccupancyRecord):
        """
        Stores the occupancy record in the database
        :param record: OccupancyRecord
        :return: None
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO OccupancyRecord (timestamp, occupancy) VALUES (?, ?)",
            (record.timestamp, record.occupancy)
        )
        conn.commit()
        conn.close()

    def get_records(self) -> dict:
        """
        Get all buffered records
        :return: dict
        """
        ret = {
            "appliance": [],
            "environmental": [],
            "occupancy": []
        }
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # appliance
        cursor.execute("SELECT * FROM ApplianceRecord")
        records = cursor.fetchall()
        for record in records:
            appliance = ApplianceRecord()
            appliance.uuid = record[0]
            appliance.timestamp = record[1]
            appliance.current = record[2]
            appliance.voltage = record[3]
            appliance.temperature = record[4]
            appliance.appliance_type = record[5]
            ret["appliance"].append(appliance)

        # environmental
        cursor.execute("SELECT * FROM EnvironmentalRecord")
        records = cursor.fetchall()
        for record in records:
            environmental = EnvironmentalRecord()
            environmental.uuid = record[0]
            environmental.timestamp = record[1]
            environmental.temperature = record[2]
            environmental.humidity = record[3]
            ret["environmental"].append(environmental)

        # occupancy
        cursor.execute("SELECT * FROM OccupancyRecord")
        records = cursor.fetchall()
        for record in records:
            occupancy = OccupancyRecord()
            occupancy.uuid = record[0]
            occupancy.timestamp = record[1]
            occupancy.occupancy = record[2]
            ret["occupancy"].append(occupancy)

        conn.close()
        return ret


    def get_records_count(self) -> int:
        """
        Get the number of buffered records
        :return: int
        """
        if self.stored_records >= 0:
            return self.stored_records
        self.stored_records = 0
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ApplianceRecord")
        self.stored_records += cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM EnvironmentalRecord")
        self.stored_records += cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM OccupancyRecord")
        self.stored_records += cursor.fetchone()[0]
        return self.stored_records

    def delete_records(self):
        """
        Delete all buffered records
        :return: None
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ApplianceRecord")
        cursor.execute("DELETE FROM EnvironmentalRecord")
        cursor.execute("DELETE FROM OccupancyRecord")
        conn.commit()
        self.stored_records = 0
