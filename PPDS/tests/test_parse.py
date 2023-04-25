import src.parse
from src.parse import (
    parse_args_string,
    split_smart,
    flat_append_in_place,
    make_arg_dict,
    scan_arglist_till_closing_bracket,
)

from PPDS.src.parse import flatten_specials


def test_flat_append_in_place():

    d1 = {"a": True, "b": 1}
    d2 = {"more": "hello"}
    flat_append_in_place(d1, "c", d2)
    assert d1 == {"a": True, "b": 1, "c_more": "hello"}


def test_flat_append_in_place_longer():

    d1 = {"a": True, "b": 1}
    d2 = {"more": "hello", "even_more": "world"}
    flat_append_in_place(d1, "c", d2)
    assert d1 == {"a": True, "b": 1, "c_more": "hello", "c_even_more": "world"}


def test_flat_append_in_place_empty():

    d1 = {"a": True, "b": 1}
    d2 = {}
    flat_append_in_place(d1, "c", d2)
    assert d1 == {"a": True, "b": 1}


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


def test_argparsing_accepts_dollar_sign():
    posargs = []
    kwargnames = ["a"]
    res = parse_args_string(r"(a=$M)", posargs, kwargnames)

    assert res == {"a": "$M"}


def test_argparsing_4():

    posargs = ["a", "long_arg_name", "c"]
    kwargnames = []
    res = parse_args_string("(1,2,3)", posargs, kwargnames)

    assert res == {"a": "1", "long_arg_name": "2", "c": "3"}


# def test_argparsing_5():
#
#     posargs = ["a", "b", "c"]
#     kwargnames = []
#     res = make_arg_dict(posargs, kwargnames, "1,2,3);more(code);")
#
#     assert res == {"a": "1", "b": "2", "c": "3"}
#
def test_scan_arglist_eat_fully():

    ls, rem = scan_arglist_till_closing_bracket("1,2,3)")
    assert rem == ""
    assert ls == ["1", "2", "3"]


def test_scan_arglist_with_brackets():

    ls, rem = scan_arglist_till_closing_bracket("1,(2,3),4)")
    assert rem == ""
    assert ls == ["1", "(2,3)", "4"]


def test_scan_arglist_with_remainder():

    ls, rem = scan_arglist_till_closing_bracket("1,2,3,4); more code...")
    assert rem == "; more code..."
    assert ls == ["1", "2", "3", "4"]


def test_flatten_special_1():

    argdict = {"a": "N : type(int)"}
    res = flatten_specials(argdict)
    assert res == {"a": "N", "a_type": "int"}


def test_flatten_special_2():

    argdict = {"a": "N : elementtype(int)"}
    res = flatten_specials(argdict)
    assert res == {"a": "N", "a_elementtype": "int"}


def test_flatten_special_3():

    argdict = {"a": "N : type(int *)"}
    res = flatten_specials(argdict)
    assert res == {"a": "N", "a_type": "int *"}


def test_flatten_special_with_multiple():

    argdict = {"a": "N : type(int), issafe(true)"}
    res = flatten_specials(argdict)
    assert res == {"a": "N", "a_type": "int", "a_issafe": True}


def test_with_simple_append():

    posargs = ["a"]
    kwargnames = []
    res = parse_args_string("(N : special)", posargs, kwargnames)

    assert res == {"a": "N", "a_special": True}


# das ganze parsen bringt wenig Mehrwert...
# lieber ein Makro, was die Argumente nimmt und dann selber eine Funktion draus macht, zB const char* - Funktion
# die Hoffnung war durch das parsen komische Funktionen zu unterstuetzen, so wie cuda-funktionen, aber das klappt eh nicht,
# wenn der parser so intolerant ist. Es ist eben parsing und nicht webscraping
#
# also was fehlt dann:
# die arr-sources so erweitern, dass Typen moeglich sind (:-Syntax, der dann einfach angehaengt wird)
# den dataclasses erlauben zu erkennen, wenn ihre Argumente nicht nur strings sondern dataclasses sind
# (--> vlt sogar verlangen als Typ?)
# die dataclasses muessen optional viele Argumente haben koennen, damit man die Funktionen damit definieren kann.
