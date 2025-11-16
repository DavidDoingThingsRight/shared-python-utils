import pytest

from tests.utils.file_cmp_test import output_test


@pytest.mark.usefixtures("output_test")
def test_stdout_1():
    print("This is a test")


@pytest.mark.usefixtures("output_test")
def test_stdout_2():
    print("This is a second test")
    print("Using Multiple Lines")
    print("!@#$%^&*()1234567890")
