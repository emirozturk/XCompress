import pytest
import os
from unittest.mock import patch
from xcompress.brute_force import brute_force_param


def test_brute_force_param_delete_except_minimum():
    input_file = "tests/data/nattest.txt"
    out_folder = "tests/data/output"
    os.makedirs(out_folder, exist_ok=True)
    
    gzip_file = "tests/data/nattest.txt.gz"
    lz_file = os.path.join(out_folder, "nattest.txt.lz4")
    
    with patch('builtins.input', return_value=""):
        brute_force_param(input_file, out_folder, delete_except_minimum=True)

    assert os.path.exists(gzip_file)
    assert not os.path.exists(lz_file)


def test_brute_force_param_keep_all():
    input_file = "tests/data/nattest.txt"
    out_folder = "tests/data/output"

    gzip_file = os.path.join(out_folder, "nattest.txt.gz")
    bz_file = os.path.join(out_folder, "nattest.txt.bz2")

    os.makedirs(out_folder, exist_ok=True)

    with patch('builtins.input', return_value=""):
        brute_force_param(input_file, out_folder, delete_except_minimum=False)

    assert os.path.exists(gzip_file)
    assert os.path.exists(bz_file)