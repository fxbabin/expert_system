import sys
import pytest
sys.path.append('..')
from es_lexer import Lexer  # noqa: E402


@pytest.mark.skip(reason="no way of currently testing this")
def tester(expression):
    res = ""
    lexer = Lexer(expression)
    try:
        res = lexer.lexer_tester()
    except Exception as e:
        res = e.__str__()
    return(res)


def test_simple_1():
    expression = "A + B => C"
    result = "A+B=>C."
    res = tester(expression)
    assert res == result


def test_simple_2():
    expression = "A + B => C + D"
    result = "A+B=>C+D."
    res = tester(expression)
    assert res == result


def test_parenthesis():
    expression = "(A + B) => C"
    result = "(A+B)=>C."
    res = tester(expression)
    assert res == result


def test_not():
    expression = "!A + B => C"
    result = "!A+B=>C."
    res = tester(expression)
    assert res == result


def test_not_2():
    expression = "A + B => !C "
    result = "A+B=>!C."
    res = tester(expression)
    assert res == result


def test_parenthesis_2():
    expression = "((A + B))) => C"
    result = "((A+B)))=>C."
    res = tester(expression)
    assert res == result


def test_simple_3():
    expression = "C => E"
    result = "C=>E."
    res = tester(expression)
    assert res == result


def test_multiple_letters():
    expression = "A + B + C => D"
    result = "A+B+C=>D."
    res = tester(expression)
    assert res == result


def test_or():
    expression = "A | B => C"
    result = "A|B=>C."
    res = tester(expression)
    assert res == result


def test_not_3():
    expression = "A + !B => F"
    result = "A+!B=>F."
    res = tester(expression)
    assert res == result


def test_not_or():
    expression = "C | !G => H"
    result = "C|!G=>H."
    res = tester(expression)
    assert res == result


def test_xor():
    expression = "V ^ W => X"
    result = "V^W=>X."
    res = tester(expression)
    assert res == result


def test_multiple_result():
    expression = "A + B => Y + Z"
    result = "A+B=>Y+Z."
    res = tester(expression)
    assert res == result


def test_or_before_and_after():
    expression = "C | D => X | V"
    result = "C|D=>X|V."
    res = tester(expression)
    assert res == result


def test_not_result():
    expression = "E + F => !V"
    result = "E+F=>!V."
    res = tester(expression)
    assert res == result


def test_if_and_only_if():
    expression = "A + B <=> C"
    result = "A+B<=>C."
    res = tester(expression)
    assert res == result


def test_not_if_and_only_if():
    expression = "A + B <=> !C"
    result = "A+B<=>!C."
    res = tester(expression)
    assert res == result


def test_complex_parentheses():
    expression = "(A + (B + C)) => D"
    result = "(A+(B+C))=>D."
    res = tester(expression)
    assert res == result


def test_error_lower_1():
    expression = "a + B => C"
    result = "Invalid character 'a' at index 1"
    res = tester(expression)
    assert res == result


def test_error_lower_2():
    expression = "A + b => C"
    result = "Invalid character 'b' at index 5"
    res = tester(expression)
    assert res == result


def test_error_no_end():
    expression = "A + B =>"
    result = "A+B=>."
    res = tester(expression)
    assert res == result


def test_error_wrong_char():
    expression = "A + B => @"
    result = "Invalid character '@' at index 10"
    res = tester(expression)
    assert res == result


def test_error_wrong_char_2():
    expression = "A  + B => @"
    result = "Invalid character '@' at index 11"
    res = tester(expression)
    assert res == result


def test_error_implies():
    expression = "A + B = > C"
    result = "Invalid character ' ' at index 8"
    res = tester(expression)
    assert res == result


def test_error_implies_2():
    expression = "A + B <= > C"
    result = "Invalid character ' ' at index 9"
    res = tester(expression)
    assert res == result


def test_error_implies_3():
    expression = "A + B >= C"
    result = "Invalid character '>' at index 7"
    res = tester(expression)
    assert res == result


def test_error_implies_4():
    expression = "A + B = C"
    result = "Invalid character ' ' at index 8"
    res = tester(expression)
    assert res == result
