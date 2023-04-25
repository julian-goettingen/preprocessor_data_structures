from __future__ import annotations

import copy
from typing import Dict, Any, List
from typeguard import check_type, typechecked

from PPDS.src import template_factory, util
from PPDS.src.config import get_config
from PPDS.src.parse import parse_args_string, make_arg_dict
from parse_err import PPDSParseError
import re

from src.parse import raw_arglist_to_argdict, raw_arglist_to_initialized_argdict


def to_dict(d):
    if isinstance(d, dict):
        return d
    return d.argdict


def expand_argdict_in_place(
    argdict: Dict[str, str],
    known_objects: Dict[str, PreprocessorDataClassInstance | dict],
):
    # hier funktioniert das expanden nicht weil im argdict irgendwie ints liegen, ausserdem die todos in parse.py beachten
    print("argdict before expand: ", argdict)
    print('known objects: ', known_objects)
    for key, val in argdict.items():
        if not isinstance(val, str):
            raise TypeError('values must be strings')
        val_stripped = val.strip()
        if val_stripped.startswith("$"):
            obj_name = val_stripped[1:]
            if obj_name in known_objects:
                argdict[key] = to_dict(known_objects[obj_name])
            else:
                raise PPDSParseError(
                    f"Referencing an unknown object: {obj_name}\n"
                    f"Known objects are: {known_objects.keys()}\n"
                )


class PreprocessorDataClassInstance:
    def __init__(
        self,
        raw_argdict: Dict[str, str],
        declare_site: str,
        klass: PreprocessorDataClass,
        known_objects: Dict[str, PreprocessorDataClassInstance],
    ):

        self.argdict = copy.deepcopy(raw_argdict)
        expand_argdict_in_place(self.argdict, known_objects)
        self.declare_site = declare_site
        self.klass = klass

    def __str__(self):
        return f"klass=<<<{self.klass}>>>, argdict=<<<{self.argdict}>>>, declare_site=<<<{self.declare_site}>>>"

    @property
    def name(self):
        try:
            return self.argdict["name"]
        except AttributeError:
            raise PPDSParseError(
                f"Dataclasses should define a 'name'-property, but this instance of {self.klass.name} has none."
            )

    def render_def(self) -> str:
        return self.klass.render_def(self.argdict, self.declare_site)

    def render_undef(self) -> str:
        return self.klass.render_undef(self.argdict, self.declare_site)


class PreprocessorDataClass:
    """
    class whose immutable instances represent the data contained in a PPDS_SOURCE-file
    that is: templates, default-arguments, constructors
    default-arguments are taken from the file unless overridden by global default-params

    parse_args creates a new python-instance of the argdict from the arguments of a constructor
    """

    def __init__(self, name, source_string, local_get_config=get_config):

        # this whole thing handles files as strings because it's easier
        self.name: str = name
        self.def_template = template_factory.get_def_template_from_source_string(
            source_string
        )
        self.undef_template = template_factory.get_undef_template_from_source_string(
            source_string
        )
        self.posargs, self.kwargs = template_factory.get_args_from_source_string(
            source_string
        )

        # global default params take precedence over defaults in header
        self.kwargs.update(local_get_config().global_default_params)

        self.constructor_list = template_factory.get_constructors_from_source_string(
            source_string
        )

    def __str__(self):

        return (
            f"args: {str(self.posargs)}, kwargs: {str(self.kwargs)}, name: {self.name}"
        )

    # a repr is actually not really the same as str but this is enough here
    def __repr__(self):
        return str(self)

    def parse_args(self, argstring) -> Dict:
        return make_arg_dict(self.posargs, self.kwargs, argstring)

    def make_instance(
        self,
        arglist: List[str],
        declare_site: str,
        known_objects: Dict[str, PreprocessorDataClassInstance],
    ) -> PreprocessorDataClassInstance:
        arg_dict = raw_arglist_to_initialized_argdict(arglist, self.posargs, self.kwargs)
        print('arg_dict initialized to this in make_instance: ', self.name, arg_dict)
        return PreprocessorDataClassInstance(
            arg_dict, declare_site=declare_site, klass=self, known_objects=known_objects
        )

    # are these even needed or better move elsewhere?

    def render_def(self, argdict, declare_site):

        res = util.header_from_template(
            self.def_template, argdict, declare_site=declare_site
        )
        return res

    def render_undef(self, argdict, declare_site):

        res = util.header_from_template(
            self.undef_template, argdict, declare_site=declare_site
        )
        return res
