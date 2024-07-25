import pytest
from unittest.mock import patch
from xcompress.select_compression import select_compression_param


def test_valid_filename_valid_config():
    input_file = "tests/data/nattest.txt"
    output_file = "tests/data/nattest.txt.gz"
    
    with patch('builtins.print') as mock_print:
        select_compression_param("gzip", input_file, output_file)
    
    contains_success_message = any("Compression completed successfully" in str(call) for call in mock_print.call_args_list)
    assert contains_success_message


def test_valid_filename_invalid_config():
    input_file = "tests/data/nattest.txt"
    output_file = "tests/data/nattest.txt.gz"
    
    with patch('builtins.print') as mock_print:
        select_compression_param("invalid_config", input_file, output_file)
    
    contains_error_message = any("Error during compression" in str(call) for call in mock_print.call_args_list)
    assert contains_error_message


def test_invalid_filename_valid_config():
    input_file = "tests/data/nonexistent.txt"
    output_file = "tests/data/nonexistent.txt.gz"
    
    with patch('builtins.print') as mock_print:
        select_compression_param("gzip", input_file, output_file)
    
    contains_error_message = any("Error during compression" in str(call) for call in mock_print.call_args_list)
    assert contains_error_message
    

def test_invalid_filename_invalid_config():
    input_file = "tests/data/nonexistent.txt"
    output_file = "tests/data/nonexistent.txt.gz"
    
    with patch('builtins.print') as mock_print:
        select_compression_param("invalid_config", input_file, output_file)
    
    contains_error_message = any("Error during compression" in str(call) for call in mock_print.call_args_list)
    assert contains_error_message
