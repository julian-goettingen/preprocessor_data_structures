import os

### full-project usage
# The prepare-step must generate the python-wrapper
# The compile-step must produce the .so-file
# So the prepare-step must know about the location of the .so-file that it does not produce
# --> .so-file-location must be in configuration.
# The .so-filename **must be used in the generated py-source**
#   but the filepath must not be used in the prepare-step (like an existence check)
#   the generated source may contain existence-checks for the .so-file
# OS-compatibility can be achieved even if generating the same code for windows and linux
# if the generated code does the checks.

### single-file usage (?)
# 1. take a file by name
# 2. copy into tempdir with a simple project
# 3. compile with a standard makefile as in the full-project-usage
# 4. make the generated code importable (?) no

### string usage (?)
# similar to above but auto-add some stuff (?)
