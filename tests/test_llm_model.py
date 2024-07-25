import pytest
from unittest.mock import patch
from xcompress.llm_model import detect_algorithm


def test_detect_algorithm():
    algorithm = detect_algorithm("tests/data/nattest.txt", "best-compression")
    assert algorithm is not None

