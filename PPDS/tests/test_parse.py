import src.parse
from src.parse import parse_args_string, split_smart


def test_split_smart_1():
    assert split_smart("a, a3==a4") == ["a", "a3==a4"]


def test_split_smart_2():
    assert split_smart("a, foo(a)") == ["a", "foo(a)"]


def test_split_smart_3():
    assert split_smart("a, foo(a,b)") == ["a", "foo(a,b)"]


def test_split_smart_4():
    assert split_smart("a, foo(a,(b==3))") == ["a", "foo(a,(b==3))"]


def test_split_smart_5():
    assert split_smart("a") == ["a"]


def test_split_smart_6():
    assert split_smart("(a==b)") == ["(a==b)"]


def test_split_smart_7():
    assert split_smart("a, (HashMap<K,V>)") == ["a", "(HashMap<K,V>)"]


def test_split_smart_8():
    assert split_smart("a[3,4], 10") == ["a[3,4]", "10"]


def test_split_smart_9():
    assert split_smart("10.0") == ["10.0"]


def test_argparsing_1():

    posargs = ["a"]
    kwargnames = ["b"]
    res = parse_args_string("(3,b=4)", posargs, kwargnames)

    assert res == {"a": "3", "b": "4"}


def test_argparsing_2():

    posargs = ["a"]
    kwargnames = ["b"]
    res = parse_args_string("(3,b=(4+3))", posargs, kwargnames)

    assert res == {"a": "3", "b": "(4+3)"}


def test_argparsing_3():

    posargs = []
    kwargnames = ["b"]
    res = parse_args_string("(b=f(3)+2)", posargs, kwargnames)

    assert res == {"b": "f(3)+2"}


def test_argparsing_4():

    posargs = ["a", "long_arg_name", "c"]
    kwargnames = []
    res = parse_args_string("(1,2,3)", posargs, kwargnames)

    assert res == {"a": "1", "long_arg_name": "2", "c": "3"}
