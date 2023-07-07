from __future__ import annotations

from typing import List
import os.path

from src.PreprocessorDataClass import PreprocessorDataClassInstance
from src.parse_err import PPDSParseError




class PPDSTargetFile:

    # minimal idea.
    # open:
    # add header/footer or frame around appends -> sections for stuff like classes maybe?
    # only write if necessary
    # better error handling if write is not possible (missing dir?)

    def __init__(self, name: str, path: str | None):
        self._name = name
        self._path = path
        self._content = []

    def append(self, s: str):
        print('appending ', s)
        self._content.append(s)

    def get_name(self):
        return self._name

    def flush(self):
        if self._path is not None:
            print(f'flushing file {self._path} with content: {self._content}')
            with open(self._path, "w") as f:
                for c in self._content:
                    f.write(c)
        else:
            print(f"not flushing file with content: {self._content} because the path is none")




def undef_filename_from_name(name: str):
    return f'"PPDS_UNDEF_{name}.h"'

def undef_filename_from_def_filename(name: str) -> str:
    prefix = 'PPDS_DEF_'
    assert name.startswith(prefix)
    return 'PPDS_UNDEF_'+name[len(prefix):]


def def_filename_from_name(name: str):
    return f'"PPDS_DEF_{name}.h"'


def get_header_file_path(dir: str, filename: str):

    return os.path.join(dir, filename)


class HeaderStack:
    def __init__(self, target_header_loc):
        self._undefs: List[PPDSTargetFile] = []
        self._defs: List[PPDSTargetFile] = []
        self.target_header_loc = target_header_loc

    def new_undef(self, name):

        def_file = self._defs.pop()
        undef_file = self._undefs.pop()

        if name != undef_file.get_name():
            raise PPDSParseError(f'Closing wrong scope. Expected {undef_file.get_name()}, got {name}')

        def_file.flush()
        undef_file.flush()

    def new_def(self, def_filename):

        hloc = self.target_header_loc
        undef_filename = undef_filename_from_def_filename(def_filename)
        defpath = get_header_file_path(hloc, def_filename)
        undefpath = get_header_file_path(hloc, undef_filename)

        self._defs.append(PPDSTargetFile(def_filename, defpath))
        self._undefs.append(PPDSTargetFile(undef_filename, undefpath))

    def new_instance(self, p: PreprocessorDataClassInstance):

        assert self._undefs
        assert self._defs

        self._undefs[-1].append(p.render_undef())
        self._defs[-1].append(p.render_def())

    def assert_empty(self):
        if len(self._undefs) == 0:
            return
        raise PPDSParseError(
            f'The following TARGET_DEF-files are not closed: {list(map(lambda x: x.name, self._defs))}\nclose them '
            f'with #include "PPDS_UNDEF_<NAME>.h"'
        )

    def __len__(self):
        assert len(self._defs) == len(self._undefs)
        return len(self._defs)
