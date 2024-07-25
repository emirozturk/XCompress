import pytest
from unittest.mock import patch
import os
from xcompress.benchmark import benchmark_param


def test_benchmark_param_compress():
    input_file = "tests/data/nattest.txt"
    output_file = "tests/data/nattest.txt.gz"

    with patch('builtins.print') as mock_print:
        benchmark_param(["gzip", "lz4"], "compress", input_file, output_file)
    
    contains_message = any("Results:" in str(call) for call in mock_print.call_args_list)
    assert contains_message


def test_benchmark_param_compress_decompress():
    input_file = "tests/data/nattest.txt"
    output_file = "tests/data/nattest.txt.gz"

    with patch('builtins.print') as mock_print:
        benchmark_param(["gzip", "lz4"], "compress_decompress", input_file, output_file)
    
    contains_message = any("Results:" in str(call) for call in mock_print.call_args_list)
    assert contains_message


def test_benchmark_param_compress():
    input_file = "tests/data/nattest.txt"
    output_file = "tests/data/nattest.txt.gz"

    with patch('builtins.print') as mock_print:
        benchmark_param(["gzip", "nonexistent"], "compress", input_file, output_file)
    
    contains_message = any("Error:" in str(call) for call in mock_print.call_args_list)
    assert contains_message


def test_benchmark_param_output_to_file():
    input_file = "tests/data/nattest.txt"
    output_file = "tests/data/nattest.txt.gz"
    output_file_json = "benchmark_results.json"

    benchmark_param(["gzip", "lz4"], "compress", input_file, output_file, output_to_file=True)

    assert os.path.exists(output_file_json)

    # Clean up generated file
    if os.path.exists(output_file_json):
        os.remove(output_file_json)


def test_benchmark_param_output_plots():
    input_file = "tests/data/nattest.txt"
    output_file = "tests/data/nattest.txt.gz"
    output_plot_file = "benchmark_plot.png"  # assuming this is the plot file name

    with patch('builtins.print') as mock_print, \
         patch('xcompress.benchmark.visualization_param') as mock_visualization:
        benchmark_param(["gzip", "lz4"], "compress", input_file, output_file, output_plots=True)
        mock_visualization.assert_called_once()
