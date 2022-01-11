import re
import sys
import util
import jinja2


# do argparsing later
files = ["example.c"]

for filename in files:
    this_file_no_ending = filename.split(".")[0]
    with open(filename, "r") as f:
        code = util.remove_comments(f.read())

    source_rex = '\#include\s+\"PPDS_(\w+?)_SOURCE.h\"'
    target_rex = '\#include\s+\"PPDS_(\w+?)_TARGET_(\w+).h\"'
    sources = re.findall(source_rex, code)
    targets = re.findall(target_rex, code)

    dsname2targetfile = {}
    dsname2template = {}
    for dsname in sources:
        if (dsname, this_file_no_ending) in targets:
            dsname2template[dsname] = jinja2.Template(util.get_template_from_source(f"PPDS_{dsname}_SOURCE.h"))
            dsname2targetfile[dsname] = open(f"PPDS_{dsname}_TARGET_{this_file_no_ending}.h", "w")
        else:
            #todo: better error handling
            print("failure")
            exit(1)

    print(dsname2targetfile)
    print(dsname2template)


    declare_rex = r"\s*PPDS_DECLARE_(\w+)(\(.*)"
    for line_no, line in enumerate(code.splitlines(),start=1):
        m = re.match(declare_rex, line)
        if m:
            dsname,raw_args = m.groups()
            
            print("line_no:", line_no)
            print("dsname:", dsname)
            print("raw_args", raw_args)

            declare_site = f"file: {filename}, line {line_no}"
            preprocessed_args = util.preprocess_raw_args(raw_args)

            header_append = util.header_from_template(dsname2template[dsname], preprocessed_args, declare_site)
            dsname2targetfile[dsname].write(header_append)

    

    for f in dsname2targetfile.values():
        f.close()



