from pathlib import Path
import pytest
import subprocess


@pytest.mark.skip(reason="no way of currently testing this")
def tester(file_name):
    file_path = Path('..') / "tests_files" / "correct_files" / file_name
    res = subprocess.run("python ../main.py -f {}".format(file_path),
                         shell=True, capture_output=True)
    return res


def test_negation_queries():
    res = tester("negation_queries.txt")
    result = 'A is False\nB is True\nC is True\nD is False\n'
    assert res.stdout.decode("utf-8") == result


def test_mixed():
    res = tester("mixed.txt")
    result = 'P is False\nN is True\nG is True\nM is True\n'
    assert res.stdout.decode("utf-8") == result


def test_and():
    res = tester("and.txt")
    result = 'C is True\nF is False\n'
    assert res.stdout.decode("utf-8") == result


def test_and_in_conclusion():
    res = tester("and_in_conclusion.txt")
    result = 'F is True\n'
    assert res.stdout.decode("utf-8") == result


def test_nested_implies():
    res = tester("nested_implies.txt")
    result = 'G is True\nF is False\n'
    assert res.stdout.decode("utf-8") == result


def test_hard():
    res = tester("hard.txt")
    result = 'J is True\n'
    assert res.stdout.decode("utf-8") == result


def test_very_hard():
    res = tester("very_hard.txt")
    result = 'T is True\nF is False\n'
    assert res.stdout.decode("utf-8") == result
