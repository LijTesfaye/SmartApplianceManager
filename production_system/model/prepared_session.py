""" Module for defining a prepared session """
import jsonschema

class PreparedSession:
    """ Class for managing a prepared session """

    def __init__(self, uuid, cur, vol, temp, e_t, e_h, occ):
        self._uuid = uuid
        self._mean_current = cur
        self._mean_voltage = vol
        self._mean_temperature = temp
        self._mean_external_temperature = e_t
        self._mean_external_humidity = e_h
        self._mean_occupancy = occ

    PREPARED_SESSION_SCHEMA = {
        "type": "object",
        "properties": {
            "uuid": {"type": ["string", "number"]},
            "mean_current": {"type": "number"},
            "mean_voltage": {"type": "number"},
            "mean_temperature": {"type": "number"},
            "mean_external_temperature": {"type": "number"},
            "mean_external_humidity": {"type": "number"},
            "mean_occupancy": {"type": "number"},
            "session_id": {"type": "string"},  # optional
            "label": {"type": "string"}  # optional
        },
        "required": [
            "uuid",
            "mean_current",
            "mean_voltage",
            "mean_temperature",
            "mean_external_temperature",
            "mean_external_humidity",
            "mean_occupancy"
        ],
        "additionalProperties": False
    }

    @staticmethod
    def from_json(data: dict)  -> "PreparedSession":
        """
        Creates a new prepared session from the given JSON data.
        Performs a validation against the preset JSON schema (PREPARED_SESSION_SCHEMA)
        """

        jsonschema.validate(instance=data, schema=PreparedSession.PREPARED_SESSION_SCHEMA)

        return PreparedSession(
            uuid=data["uuid"],
            cur=data["mean_current"],
            vol=data["mean_voltage"],
            temp=data["mean_temperature"],
            e_t=data["mean_external_temperature"],
            e_h=data["mean_external_humidity"],
            occ=data["mean_occupancy"]
        )

    def to_tuple(self):
        """ Converts the prepared session to a tuple. Excludes the uuid """
        return (
            self._mean_current,
            self._mean_voltage,
            self._mean_temperature,
            self._mean_external_temperature,
            self._mean_external_humidity,
            self._mean_occupancy
        )

    def get_uuid(self):
        """ Gets the UUID of the prepared session """
        return self._uuid
