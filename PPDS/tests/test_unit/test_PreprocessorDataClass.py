import pytest
from typing import Dict

import typeguard
from src.PreprocessorDataClass import expand_argdict_in_place

from src.parse_err import PPDSParseError

from src.PreprocessorDataClass import PreprocessorDataClassInstance


def test_expand_argdict_empty():

    argdict = {"a": "a_val", "b": "b_val"}
    known_names = {}

    expand_argdict_in_place(argdict, known_names)

    assert argdict == {"a": "a_val", "b": "b_val"}


def test_expand_argdict_simple():

    argdict = {"a": "a_val", "b": "$b_obj"}
    known_names = {"b_obj": {"more": "stuff"}}

    expand_argdict_in_place(argdict, known_names)

    assert argdict == {"a": "a_val", "b": {"more": "stuff"}}


def test_expand_argdict_with_whitespace():

    argdict = {"a": "a_val", "b": " $b_obj  "}
    known_names = {"b_obj": {"more": "stuff"}}

    expand_argdict_in_place(argdict, known_names)

    assert argdict == {"a": "a_val", "b": {"more": "stuff"}}


def test_expand_argdict_with_multiple():

    argdict = {"a": "a_val", "b": "$b_obj ", "c": "$c_obj"}
    known_names = {"b_obj": {"more": "stuff"}, "c_obj": {"even": "more"}, "d_obj": {"something": "else"}}

    expand_argdict_in_place(argdict, known_names)

    assert argdict == {"a": "a_val", "b": {"more": "stuff"}, "c": {"even": "more"}}


def test_expand_argdict_name_error():

    argdict = {"a": "a_val", "b": "$b_obj "}
    known_names = {"c_obj": {"even": "more"}, "d_obj": {"something": "else"}}

    with pytest.raises(PPDSParseError, match=r"unknown object: b_obj") as e:
        expand_argdict_in_place(argdict, known_names)
    print(type(e))
    print(e.value.__class__)
    print(PPDSParseError("duh").__class__)
    print(type(PPDSParseError("duh")))
    print(e)
    assert e.errisinstance(PPDSParseError)

def test_expand_argdict_with_varargs():

    argdict = {"a": "a_val", "var_args": ["$b_obj ", "$c_obj", "nonexpanded"]}
    known_names = {"b_obj": {"more": "stuff"}, "c_obj": {"even": "more"}, "d_obj": {"something": "else"}}

    expand_argdict_in_place(argdict, known_names)
    assert argdict == {"a": "a_val", "var_args": [{"more": "stuff"}, {"even": "more"}, "nonexpanded"]}
