import pytest
from unittest.mock import patch, mock_open
from xcompress.create_config import get_config_input, save_config_to_file, create_config_param, create_config

@pytest.fixture
def sample_config():
    return {
        "name": "test",
        "executable_path": "/usr/bin/test",
        "input_file_param": "--input {input_file}",
        "output_file_param": "--output {output_file}",
        "compression_params": ["-c", "-v"],
        "decompression_params": ["-d", "-k"],
        "extension": "tse"
    }


def test_get_config_input():
    with patch('builtins.input', side_effect=["testalg", "test", "-i ", "-o ", "-c,-v,-f", "-d,-k", "tse"]), \
        patch('builtins.print'):
        
        config = get_config_input()
        
        assert config["name"] == "testalg"
        assert config["executable_path"] == "test"
        assert config["input_file_param"] == "-i {input_file}"
        assert config["output_file_param"] == "-o {output_file}"
        assert config["compression_params"] == ["-c", "-v", "-f"]
        assert config["decompression_params"] == ["-d", "-k"]
        assert config["extension"] == "tse"


def test_create_config_param():
    config = create_config_param("testalg", "test", "-i ", "-o ", ["-c", "-v","-f"], ["-d", "-k"], "tse")
    assert config["name"] == "testalg"
    assert config["executable_path"] == "test"
    assert config["input_file_param"] == "-i {input_file}"
    assert config["output_file_param"] == "-o {output_file}"
    assert config["compression_params"] == ["-c", "-v","-f"]
    assert config["decompression_params"] == ["-d", "-k"]
    assert config["extension"] == "tse"