class RecordsBuffer:
    def __init__(self):
        self.stored_records = []

    def store_record(self, record):
        self.stored_records.append(record)

    def get_records(self):
        return self.stored_records

    def delete_records(self):
        self.stored_records = []