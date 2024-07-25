import pytest
from unittest.mock import patch, Mock
import readchar
from xcompress.csm import model_compression_param, print_menu

@pytest.fixture
def menu_options():
    return ["Back to main menu", "Fast Compression", "Fast Decompression", "Best Compression"]


def test_print_menu(capsys, menu_options):
    with patch('xcompress.clear_screen'):
        selected_row = 1
        print_menu(selected_row, menu_options)
        captured = capsys.readouterr()
        assert "Select Compression Mode:" in captured.out
        assert "\033[1;32m->\033[0m \033[1;32m Fast Compression \033[0m" in captured.out


@patch('builtins.input', return_value='')
def test_model_compression_param_successful(mock_input, capsys):
    model_compression_param('fast-compress', 'tests/data/nattest.txt', 'nattest.cmp')
    captured = capsys.readouterr()
    assert "Compression completed successfully" in captured.out
