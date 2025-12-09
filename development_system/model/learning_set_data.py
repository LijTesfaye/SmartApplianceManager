
class LearningDataSet:
    _instance = {}
    def __init__(self):
        pass

    @staticmethod
    def set_from_external_format(data):
            """
            Converts external JSON data of the form:
            { "training": [...], "validation": [...], "test": [...] }
            into internal format used by the system.
            """
            mapped = {
                "train": {"data": [], "labels": []},
                "validation": {"data": [], "labels": []},
                "test": {"data": [], "labels": []},
            }

            label_map = {"none": 0, "overheating": 1, "electrical": 2}
            for phase, records in data.items():
                # normalize the key name (training -> train)
                key = "train" if phase == "training" else phase
                for rec in records:
                    mapped[key]["data"].append(rec["features"])
                    mapped[key]["labels"].append(label_map.get(rec["label"], -1))

            LearningDataSet._instance = mapped
            print("[INFO] External dataset loaded into LearningDataSet.")

    @staticmethod
    def set_data(data):
        LearningDataSet._instance = {
            "training" : {
                "data": {
                    "mean_current":[],
                    "mean_voltage":[],
                    "mean_temperature":[],
                    "mean_external_temperature":[],
                    "mean_external_humidity":[],
                    "mean_occupancy":[]
                },
                "labels" : [],
            },
            "validation" : {
                "data": {
                    "mean_current":[],
                    "mean_voltage":[],
                    "mean_temperature":[],
                    "mean_external_temperature":[],
                    "mean_external_humidity":[],
                    "mean_occupancy":[]
                },
                "labels" : [],
            },
            "test" : {
                "data": {
                    "mean_current":[],
                    "mean_voltage":[],
                    "mean_temperature":[],
                    "mean_external_temperature":[],
                    "mean_external_humidity":[],
                    "mean_occupancy":[]
                },
                "labels" : [],
            }
        }

        categories = ["training", "validation", "test"]
        for category in categories:
            for feature in data[category]:
                label = feature["label"]
                LearningDataSet._instance[category]["labels"].append(label)
                LearningDataSet._instance[category]["data"]["mean_current"].append(feature["features"][0])
                LearningDataSet._instance[category]["data"]["mean_voltage"].append(feature["features"][1])
                LearningDataSet._instance[category]["data"]["mean_temperature"].append(feature["features"][2])
                LearningDataSet._instance[category]["data"]["mean_external_temperature"].append(feature["features"][3])
                LearningDataSet._instance[category]["data"]["mean_external_humidity"].append(feature["features"][4])
                LearningDataSet._instance[category]["data"]["mean_occupancy"].append(feature["features"][5])

    @staticmethod
    def get_data(category):
        if category not in LearningDataSet._instance:
            raise KeyError(f"[ERROR] '{category}' data not found. Make sure set_data() or set_from_external_format() was called.")
        return LearningDataSet._instance[category]

