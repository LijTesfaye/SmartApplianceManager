class RawSessionSchemaVerifier:

    def verify(self, data: dict):
        self._require_keys(data, ["UUID", "applianceRecords", "environmentalRecords",
                                  "occupancyRecords", "expertRecord"])

        self._verify_uuid(data["UUID"])
        self._verify_appliance_records(data["applianceRecords"])
        self._verify_environmental_records(data["environmentalRecords"])
        self._verify_occupancy_records(data["occupancyRecords"])
        self._verify_expert_record(data["expertRecord"])

        return True

    def _verify_uuid(self, value):
        if not isinstance(value, int):
            raise ValueError(f"uuid must be int, found {type(value)}")

    def _verify_appliance_records(self, items):
        if not isinstance(items, list):
            raise ValueError("applianceRecords must be a list")

        for entry in items:
            self._require_keys(entry, ["UUID", "timestamp", "current", "voltage",
                                       "temperature", "appliance_type"])

            self._verify_uuid(entry["UUID"])
            self._verify_string(entry["timestamp"])
            self._verify_float(entry["current"])
            self._verify_float(entry["voltage"])
            self._verify_float(entry["temperature"])
            self._verify_string(entry["appliance_type"])

    def _verify_environmental_records(self, items):
        if not isinstance(items, list):
            raise ValueError("environmentalRecords must be a list")

        for entry in items:
            self._require_keys(entry, ["UUID", "timestamp", "temperature", "humidity"])

            self._verify_uuid(entry["UUID"])
            self._verify_string(entry["timestamp"])
            self._verify_float(entry["temperature"])
            self._verify_float(entry["humidity"])

    def _verify_occupancy_records(self, items):
        if not isinstance(items, list):
            raise ValueError("occupancyRecords must be a list")

        for entry in items:
            self._require_keys(entry, ["UUID", "timestamp", "occupancy"])

            self._verify_uuid(entry["UUID"])
            self._verify_string(entry["timestamp"])
            self._verify_float(entry["occupancy"])

    def _verify_expert_record(self, entry):
        if not isinstance(entry, dict):
            raise ValueError("expertRecord must be an object")

        self._require_keys(entry, ["UUID", "timestamp", "label"])

        if entry["UUID"] is not None:
            self._verify_uuid(entry["UUID"])

        if entry["timestamp"] is not None:
            self._verify_string(entry["timestamp"])

        if entry["label"] is not None:
            self._verify_string(entry["label"])

    def _verify_string(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError(f"String expected, found {type(value)}")

    def _verify_float(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError(f"Number expected, found {type(value)}")

    def _require_keys(self, obj, required):
        if not isinstance(obj, dict):
            raise ValueError(f"Object expected, found {type(obj)}")

        missing = [k for k in required if k not in obj]
        if missing:
            raise ValueError(f"Missing keys: {missing} in {obj}")
