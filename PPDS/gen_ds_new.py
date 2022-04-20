import re
import sys
import util
import jinja2
import json

#TODO: must allow this to be in another directory
SOURCE_REX = '\#include\s+\"PPDS_SOURCE_(\w+?).h\"'


class PreprocessorDataClass():

    def __init__(self, name, source_string):

        # TODO: Is it smart to use the file as a string and not string?
        # meh, it's easier
        self.name = name
        self.source_string = source_string
        self.def_template = util.get_def_template_from_source_string(source_string)
        self.undef_template = util.get_undef_template_from_source_string(source_string)
        self.args, self.kwargs = util.get_args_from_source_string(source_string)

    def __str__(self):

        return f"args: {str(self.args)}, kwargs: {str(self.kwargs)}, name: {self.name}"

    # TODO: this is a bit incorrect
    def __repr__(self):
        return str(self)


# argparsing late   r
files = ["example.c"]

for filename in files:

    with open(filename, "r") as f:
        # preserves line numbers
        code = util.remove_comments(f.read())

    source_names = re.findall(SOURCE_REX, code)
    source_strings = []
    pp_dataclasses = []
    for name in source_names:
        source_filename = f"PPDS_SOURCE_{name}.h"
        with open(source_filename) as f:
            source_string = f.read()
        source_strings.append(source_string)
        pp_dataclasses.append(PreprocessorDataClass(name, source_string))

    print(pp_dataclasses)
