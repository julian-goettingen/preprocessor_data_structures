from src.template_factory import parse_yaml_args
from src.parse import make_arg_dict

from src.parse import raw_arglist_to_initialized_argdict


def test_parse_yaml_args_standard():

    args = """
args:
    - name
    - size
kwargs:
    skip_checks: "0"
    panic: exit(1)
    """

    res = parse_yaml_args(args)

    assert res == (["name", "size"], {"skip_checks": "0", "panic": "exit(1)"})


# was will ich noch:
# - varargs support
# - Fehlermeldungen vernünftig
# - validations gleich reintun?
# - computed properties gleich darin definieren?
# - type coercions wie es sinnvoll ist?
# - __ im Variablennamen reservieren?

# die Ergebnisse von parse_yaml_args werden letzendlich in make_arg_dict gegeben.
# mit den beiden Sachen kann man die Konstruktoren supper testen
def test_parse_yaml_args_with_some_defaults():

    args = """
args:
    - name
kwargs:
    kw: "0"
    more: "default"
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "kw=world"], args, kwargs)

    assert res == {"name": "hello", "kw": "world", "more": "default"}


def test_parse_yaml_args_with_varargs_single():

    args = """
args:
    - name
    - _var_args_
kwargs: {}
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "A"], args, kwargs)

    assert res == {"name": "hello", "var_args": ["A"]}

def test_parse_yaml_args_with_varargs_multiple():

    args = """
args:
    - name
    - _var_args_
kwargs: {}
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "A", "B", "C"], args, kwargs)

    assert res == {"name": "hello", "var_args": ["A", "B", "C"]}


def test_parse_yaml_args_no_kwargs_no_varargs():

    args = """
args:
    - name
kwargs: {}
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello"], args, kwargs)

    assert res == {"name": "hello"}


def test_parse_yaml_args_with_varargs_empty():

    args = """
args:
    - name
    - _var_args_
kwargs: {}
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello"], args, kwargs)

    assert res == {"name": "hello", "var_args": []}

def test_parse_yaml_args_with_varargs_only_multiple():

    args = """
args:
    - _var_args_
kwargs: {}
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "world"], args, kwargs)

    assert res == {"var_args": ["hello", "world"]}

def test_parse_yaml_args_with_varargs_only_single():

    args = """
args:
    - _var_args_
kwargs: {}
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello"], args, kwargs)

    assert res == {"var_args": ["hello"]}


def test_parse_yaml_args_with_varargs_only_empty():

    args = """
args:
    - _var_args_
kwargs: {}
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict([], args, kwargs)

    assert res == {"var_args": []}


def test_parse_yaml_args_with_varargs_only_multiple_unused_kw():

    args = """
args:
    - _var_args_
kwargs:
    kw: something
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "world"], args, kwargs)

    assert res == {"var_args": ["hello", "world"], "kw": "something"}

def test_parse_yaml_args_with_varargs_only_single_unused_kw():

    args = """
args:
    - _var_args_
kwargs:
    kw: something
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello"], args, kwargs)

    assert res == {"var_args": ["hello"], "kw": "something"}


def test_parse_yaml_args_with_varargs_only_empty_unused_kw():

    args = """
args:
    - _var_args_
kwargs:
    kw: something
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict([], args, kwargs)

    assert res == {"var_args": [], "kw": "something"}


def test_parse_yaml_args_with_varargs_only_multiple_kw_used():

    args = """
args:
    - _var_args_
kwargs:
    kw: something
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "world", "kw=used"], args, kwargs)

    assert res == {"var_args": ["hello", "world"], "kw": "used"}

def test_parse_yaml_args_with_varargs_only_single_kw_used():

    args = """
args:
    - _var_args_
kwargs:
    kw: something
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "kw= used"], args, kwargs)

    assert res == {"var_args": ["hello"], "kw": "used"}


def test_parse_yaml_args_with_varargs_only_empty_kw_used():

    args = """
args:
    - _var_args_
kwargs:
    kw: something
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["kw=used"], args, kwargs)

    assert res == {"var_args": [], "kw": "used"}


def test_parse_yaml_args_with_varargs_multiple_followed_by_kwargs():

    args = """
args:
    - name
    - _var_args_
kwargs:
    kw: "default"
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "A", "B", "C", "kw=nondefault"], args, kwargs)

    assert res == {"name": "hello", "var_args": ["A", "B", "C"], "kw":"nondefault"}


def test_parse_yaml_args_with_varargs_empty_followed_by_kwargs():

    args = """
args:
    - name
    - _var_args_
kwargs:
    kw: "default"
    """

    args, kwargs = parse_yaml_args(args)
    res = raw_arglist_to_initialized_argdict(["hello", "kw = nondefault"], args, kwargs)

    assert res == {"name": "hello", "var_args": [], "kw":"nondefault"}


