from __future__ import annotations
from typing import Dict, Any

from PPDS.src import template_factory, util
from PPDS.src.config import get_config
from PPDS.src.parse import parse_args_string, make_arg_dict
from parse_err import PPDSParseError
import re


def expand_argdict_in_place(argdict: Dict[str, Any], known_objects: Dict[str, Any]):

    for key, val in argdict.items():
        val_stripped = val.strip()
        if val_stripped.startswith("$"):
            obj_name = val_stripped[1:]
            if obj_name in known_objects:
                argdict[key] = known_objects[obj_name]
            else:
                raise PPDSParseError(
                    f"Referencing an unknown object: {obj_name}\n"
                    f"Known objects are: {known_objects.keys()}\n"
                )


class PreprocessorDataClassInstance:
    def __init__(
        self, argdict: Dict[str, str], declare_site: str, klass: PreprocessorDataClass
    ):

        self.argdict = argdict
        self.declare_site = declare_site
        self.klass = klass
        self.is_expanded = False

    def render_def(self):
        pass


class PreprocessorDataClass:
    """
    class whose immutable instances represent the data contained in a PPDS_SOURCE-file
    that is: templates, default-arguments, constructors
    default-arguments are taken from the file unless overridden by global default-params

    parse_args creates a new python-instance of the argdict from the arguments of a constructor
    """

    def __init__(self, name, source_string, local_get_config=get_config):

        # this whole thing handles files as strings because it's easier
        self.name = name
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
