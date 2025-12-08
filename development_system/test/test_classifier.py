
import os
import sys
import pytest
from flask.cli import load_dotenv



print("[DEBUG] COMMUNICATION_SYSTEM_CONFIG:", os.getenv("COMMUNICATION_SYSTEM_CONFIG"))


#sys.path.insert(0, r'../../development_system')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from development_system.model.learning_set_data import LearningDataSet
from development_system.utility.json_read_write import JsonReadWrite
from development_system.controller.development_system_localtest import DevelopmentSystemOrchestratorLocalhost


@pytest.fixture
def dataset():
    print("")
    print("1st fixture")
    path = os.getenv("SAMPLE_DATASET")
    res, file_content = JsonReadWrite.read_json_file(path)
    return LearningDataSet.set_from_external_format(file_content)

@pytest.fixture
def system():
    print("************************************")
    print("2nd fixture")
    return DevelopmentSystemOrchestratorLocalhost() #DevelopmentSystemOrchestratorLocalhost

def test_chain(dataset , system):
    system.update_stage("set_avg_hyp")
    system.run(automated=True)

    # Learning phase
    assert os.path.isfile(os.getenv("TEST_IMAGE_DIR")) is True

    # Validation phase
    assert os.path.isfile(os.getenv("VALIDATION_TEST_REPORT_PATH")) is True

    # Test Phase
    assert os.path.isfile(os.getenv("TEST_REPORT_PATH")) is True

    # winner  classifier
    assert os.path.isfile(os.getenv("TEST_WINNER_CLASSIFIER")) is True