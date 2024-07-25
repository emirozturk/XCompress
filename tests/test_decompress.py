import pytest
from unittest.mock import patch, mock_open, MagicMock
from xcompress.decompress import decompress_with_config

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
    process_mock = MagicMock()
    attrs = {'wait.return_value': 0}
    process_mock.configure_mock(**attrs)
    mock_popen.return_value = process_mock

    input_file = "test.txt.gz"

    result = decompress_with_config(valid_config, input_file)

    assert result[0] == "test.o.txt"
    assert isinstance(result[1], float)


@patch('shutil.which', return_value=None)
@patch('subprocess.Popen')
def test_compress_with_no_valid_executable(mock_popen, mock_which, config_with_no_valid_executable, capsys):
    input_file = "test.txt.gz"
    
    result_output_file, execution_time_ns = decompress_with_config(config_with_no_valid_executable, input_file)

    assert result_output_file == ""
    assert execution_time_ns == 0

    captured = capsys.readouterr()
    assert "An error occurred: Executable nec not found on the system" in captured.out

    mock_popen.assert_not_called()