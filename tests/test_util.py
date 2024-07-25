import pytest
from unittest.mock import patch, mock_open
import os
import json
from xcompress.util import clear_screen, load_configs, get_config, count_unique_symbols, round_to_class, bin_usc, get_file_size


@pytest.fixture
def zlibconf():
    return {
        "name": "zlib",
        "executable_path": "pigz",
        "input_file_param":"{input_file}",
        "output_file_param":"stdout",
        "compression_params": ["-c","-k","-f", "@input_file_param"],
        "decompression_params": ["-d","-k","-f","-c", "@input_file_param"],
        "extension": "gz"
    }

def test_clear_screen_unix():
    with patch('os.system') as mock_system, patch('platform.system', return_value='Linux'):
        clear_screen()
        mock_system.assert_called_once_with('clear')


def test_clear_screen_windows():
    with patch('os.system') as mock_system, patch('platform.system', return_value='Windows'):
        clear_screen()
        mock_system.assert_called_once_with('cls')


def test_round_to_class():
    assert round_to_class(1000) == '1kb'
    assert round_to_class(10000) == '10kb'
    assert round_to_class(100000) == '100kb'
    assert round_to_class(1000000) == '1mb'
    assert round_to_class(10000000) == '10mb'
    assert round_to_class(110000000) == '100mb'


def test_bin_usc():
    assert bin_usc(123) == 100
    assert bin_usc(49) == 0
    assert bin_usc(50) == 50
    assert bin_usc(151) == 150


def test_load_configs():
    configs = load_configs('../xcompress/compression_configs')
    assert len(configs) == 13
    assert configs[0]['name'] == 'brotli'


def test_get_config_found(zlibconf):
    configs = load_configs('../xcompress/compression_configs')
    config = get_config(configs, 'zlib')
    assert config == zlibconf


def test_get_config_not_found():
    configs = load_configs('../xcompress/compression_configs')
    config = get_config(configs, 'nonexistingalg')
    assert config is None


def test_count_unique_symbols():
    with patch('builtins.open', mock_open(read_data='this is an example data for testing chars and it has special chars too öçşiğü')):
        count = count_unique_symbols('dummy/path')
        assert count == 23

