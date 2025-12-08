
import os
import sys
import pytest
sys.path.insert(0, r'../../development_system')
from development_system.generator.report_generator import ReportGenerator

@pytest.fixture
def json_file_path():
    return os.getenv("TEST_REPORT_PATH")

@pytest.fixture
def data():
    return {
        "key" : "value",
        "key2" : "value" ,
        "key3" : "value"
    }

def test_json_file(data, json_file_path):

    test_report_generator = ReportGenerator(report_type="test",
                                            test_result=data)
    test_report_generator.generate_report()
    assert os.path.isfile(json_file_path) is True

