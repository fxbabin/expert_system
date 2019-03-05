import sys
import pytest
sys.path.append('..')
from xs_lexer import Lexer  # noqa: E402
from xs_parser import Parser  # noqa: E402

out = ""


@pytest.mark.skip(reason="no way of currently testing this")
def tester(expression):
    global out
    out = ""
    res = ""
    try:
        lexer = Lexer(expression)
        parser = Parser(lexer)
        root = parser.parse()
        get_prefix_run(root)
        res = out
    except Exception as e:
        res = e.__str__()
    return(res)


@pytest.mark.skip(reason="no way of currently testing this")
def get_prefix_run(node):
    global out
    if node:
        if type(node).__name__ == "Node_letter":
            out += node.token.value
        if type(node).__name__ == "Node_condition":
            get_prefix_run(node.left)
            out += node.token.value
            get_prefix_run(node.right)


def test_plus_at_beginning():
    expression = "+ A + B => C"
    result = "Invalid character '+' at index 1"
    res = tester(expression)
    assert res == result


def test_plus_at_end():
    expression = "A + B => C +"
    result = "Invalid character '+' at index 12"
    res = tester(expression)
    assert res == result


def test_plus_before_equal():
    expression = "A + B + => C"
    result = "Invalid character '=' at index 9"
    res = tester(expression)
    assert res == result


def test_plus_after_equal():
    expression = "A + B => + C"
    result = "Invalid character '+' at index 10"
    res = tester(expression)
    assert res == result


def test_lower_char():
    expression = "a + B => C"
    result = "Invalid character 'a' at index 1"
    res = tester(expression)
    assert res == result


def test_special_char():
    expression = "A + B => @"
    result = "Invalid character '@' at index 10"
    res = tester(expression)
    assert res == result


def test_multiple_letters():
    expression = "AB + C => D"
    result = "Invalid character 'B' at index 2"
    res = tester(expression)
    assert res == result


def test_multiple_letters_2():
    expression = "A + B => CD"
    result = "Invalid character 'D' at index 11"
    res = tester(expression)
    assert res == result


def test_wrong_parenthesis():
    expression = "A + B => ((C)"
    result = "Invalid syntax : could not find match of parenthesis"
    res = tester(expression)
    assert res == result


def test_parenthesis_beyond_equal():
    expression = "((A + B) => C)"
    result = "A+B=>C"
    res = tester(expression)
    assert res == result


def test_double_or():
    expression = "A || B => C"
    result = "Invalid character '|' at index 4"
    res = tester(expression)
    assert res == result


def test_double_implies():
    expression = "A + B => C => D "
    result = "Invalid syntax : Too many equals signs"
    res = tester(expression)
    assert res == result


def test_triple_implies():
    expression = "A + B => C => D => E "
    result = "Invalid syntax : Too many equals signs"
    res = tester(expression)
    assert res == result


def test_double_only_if():
    expression = "A + B <=> C <=> D"
    result = "Invalid syntax : Too many equals signs"
    res = tester(expression)
    assert res == result


def test_double_only_if_without_right():
    expression = "A + B <=> C <=>"
    result = "Invalid character '<' at index 13"
    res = tester(expression)
    assert res == result


def test_wrong_end():
    expression = "A + B => C >"
    result = "Invalid character 'EOL' at index 13"
    res = tester(expression)
    assert res == result


def test_wrong_operator():
    expression = "A < B => C"
    result = "Invalid character ' ' at index 4"
    res = tester(expression)
    assert res == result


def test_wrong_equal():
    expression = "A + B ==> C"
    result = "Invalid character '=' at index 8"
    res = tester(expression)
    assert res == result


def test_wrong_only_if():
    expression = "A + B <==> C"
    result = "Invalid character '=' at index 9"
    res = tester(expression)
    assert res == result
