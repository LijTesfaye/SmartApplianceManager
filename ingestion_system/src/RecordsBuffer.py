import sqlite3

from ingestion_system.src.records.ApplianceRecord import ApplianceRecord
from ingestion_system.src.records.EnvironmentalRecord import EnvironmentalRecord
from ingestion_system.src.records.OccupancyRecord import OccupancyRecord


class RecordsBuffer:
    db_name: str
    stored_records: int

    def __init__(self):
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

    def store_record(self, record):
        if isinstance(record, ApplianceRecord):
            self.store_appliance(record)
        elif isinstance(record, EnvironmentalRecord):
            self.store_environmental(record)
        elif isinstance(record, OccupancyRecord):
            self.store_occupancy(record)
        self.stored_records += 1


    def store_appliance(self, record: ApplianceRecord):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
        "INSERT INTO ApplianceRecord (timestamp, current, voltage, temperature, applianceType) VALUES (?, ?, ?, ?, ?)",
    (record.timestamp, record.current, record.voltage, record.temperature, record.appliance_type)
        )
        conn.commit()
        conn.close()

    def store_environmental(self, record: EnvironmentalRecord):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO EnvironmentalRecord (timestamp, temperature, humidity) VALUES (?, ?, ?)",
            (record.timestamp, record.temperature, record.humidity)
        )
        conn.commit()
        conn.close()

    def store_occupancy(self, record: OccupancyRecord):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO OccupancyRecord (timestamp, occupancy) VALUES (?, ?)",
            (record.timestamp, record.occupancy)
        )
        conn.commit()
        conn.close()

    def get_records(self) -> dict:
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


    def get_records_count(self):
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
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ApplianceRecord")
        cursor.execute("DELETE FROM EnvironmentalRecord")
        cursor.execute("DELETE FROM OccupancyRecord")
        conn.commit()
        self.stored_records = 0
