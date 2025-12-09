def _mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


class Extractor:
    def __init__(self, raw_session: dict):
        self.raw = raw_session

    def extract(self) -> dict:
        appliance = self.raw.get("applianceRecords", [])
        env = self.raw.get("environmentalRecords", [])
        occ = self.raw.get("occupancyRecords", [])
        expert = self.raw.get("expertRecord", {})
        mean_current = _mean([x.get("current") for x in appliance])
        mean_voltage = _mean([x.get("voltage") for x in appliance])
        mean_temperature = _mean([x.get("temperature") for x in appliance])
        mean_external_temperature = _mean([x.get("temperature") for x in env])
        mean_external_humidity = _mean([x.get("humidity") for x in env])
        mean_occupancy = _mean([x.get("occupancy") for x in occ])

        return {
            "UUID": self.raw.get("UUID"),
            "label": expert.get("label"),
            "mean_current": mean_current,
            "mean_voltage": mean_voltage,
            "mean_temperature": mean_temperature,
            "mean_external_temperature": mean_external_temperature,
            "mean_external_humidity": mean_external_humidity,
            "mean_occupancy": mean_occupancy
        }
