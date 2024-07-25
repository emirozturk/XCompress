import subprocess
import timeit
import pytest
from unittest.mock import patch
from xcompress.compress import compress_with_config

@pytest.fixture
def valid_config():
    return {
        "name": "gzip",
        "executable_path": "gzip",
        "input_file_param":"{input_file}",
        "output_file_param":"stdout",
        "compression_params": ["-c","-k","-f", "@input_file_param"],
        "decompression_params": ["-d","-k","-f","-c", "@input_file_param"],
        "extension": "gz"
    }

@pytest.fixture
def config_with_no_valid_executable():
    return {
        "name": "nonexistingcomrpessor",
        "executable_path": "nec",
        "input_file_param":"{input_file}",
        "output_file_param":"stdout",
        "compression_params": ["-c","-k","-f", "@input_file_param"],
        "decompression_params": ["-d","-k","-f","-c", "@input_file_param"],
        "extension": "nc"
    }

@patch('subprocess.Popen')
def test_compress_with_valid_config(mock_popen, valid_config):
    input_file = "test.txt"
    output_file = "test.txt.gz"
    
    result_output_file, execution_time_ns = compress_with_config(valid_config, input_file)
    
    assert result_output_file == output_file
    assert execution_time_ns > 0
    mock_popen.assert_called_once()

@patch('subprocess.Popen')
def test_compress_with_no_valid_executable(mock_popen, config_with_no_valid_executable):
    input_file = "test.txt"
    
    result_output_file, execution_time_ns = compress_with_config(config_with_no_valid_executable, input_file)
    
    assert result_output_file == ""
    assert execution_time_ns == 0
    mock_popen.assert_not_called()

@patch('subprocess.Popen')
def test_compress_with_output_provided(mock_popen, valid_config):
    input_file = "test.txt"
    output_file = "test-output.gz"
    
    result_output_file, execution_time_ns = compress_with_config(valid_config, input_file, output_file)
    
    assert result_output_file == output_file
    assert execution_time_ns > 0
    mock_popen.assert_called_once()



@patch('subprocess.Popen')
def test_compress_with_exception(mock_popen, valid_config):
    mock_popen.side_effect = Exception("Mocked exception")
    
    input_file = "test.txt"
    
    result_output_file, execution_time_ns = compress_with_config(valid_config, input_file)
    
    assert result_output_file == ""
    assert execution_time_ns == 0
    mock_popen.assert_called_once()
