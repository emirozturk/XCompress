import pytest
from unittest.mock import patch, mock_open
from xcompress.visualization import read_results_from_file, visualization_param  
import json


@pytest.fixture
def benchmark_result():
    return [
                {
                    "filename": "nattest.txt",
                    "name": "gzip",
                    "file_size": 1028,
                    "compressed_size": 651,
                    "compression_time_ns": 7576083.997264504,
                    "decompression_time_ns": 4941208.986565471
                },
                {
                    "filename": "nattest.txt",
                    "name": "lz4",
                    "file_size": 1028,
                    "compressed_size": 916,
                    "compression_time_ns": 5006290.972232819,
                    "decompression_time_ns": 4168999.847024679
                }
            ]


def test_read_results_from_file(benchmark_result):
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=json.dumps(benchmark_result))):
        results = read_results_from_file('tests/data/benchmark_results.json')
        
        assert len(results) == 2

        assert results[0]['filename'] == 'nattest.txt'
        assert results[0]['name'] == "gzip"
        assert results[0]['file_size'] == 1028
        assert results[0]['compressed_size'] == 651
        assert results[0]['compression_time_ns'] == 7576083.997264504
        assert results[0]['decompression_time_ns'] == 4941208.986565471

        assert results[1]['filename'] == 'nattest.txt'
        assert results[1]['name'] == "lz4"
        assert results[1]['file_size'] == 1028
        assert results[1]['compressed_size'] == 916
        assert results[1]['compression_time_ns'] == 5006290.972232819
        assert results[1]['decompression_time_ns'] == 4168999.847024679


def test_read_results_from_file_not_found(capfd):
    with patch('os.path.exists', return_value=False):
        results = read_results_from_file('missing.json')
        assert not results
        out, _ = capfd.readouterr()
        assert "File not found: missing.json" in out


@patch('plotly.graph_objects.Bar')
@patch('plotly.graph_objects.Figure')
def test_visualization_param(mock_figure, mock_bar,benchmark_result):
    test_results = benchmark_result
    with patch('xcompress.visualization.read_results_from_file', return_value=test_results):
        visualization_param('tests/data/benchmark_result.json')
        assert mock_bar.called
        assert mock_figure.called


@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('plotly.graph_objects.Figure.show'), \
         patch('plotly.graph_objects.Figure.update_layout'):
        yield

