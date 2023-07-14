#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
args:
    - name
    - _var_args_
kwargs:
    skip_checks: NDEBUG
    panic: exit(1)
    print_base: PRINT
*/

/* PPDS_CONSTRUCTORS:
[
    "\\s*PPDS_DECLARE_SOURCE_FUNCTION_NEW(\\(.*)"
]
 */

/* PPDS_DEFS_FOR_HEADER:

// a 'function call' is actually this macro expansion
#define {{name}}({%- for arg in var_args -%}
{{arg}}{{", " if not loop.last else ""}}
{%- endfor -%}) {{name}}_def({%- for arg in var_args -%}
{%- if arg.type is defined -%}
{{arg}}
{%- elif arg.ptype is defined -%}
{{arg}} ## _expand_for_call (arg)
{%- endif -%}
{{", " if not loop.last else "" }}
{%- endfor -%})

// for the function declaration/definition
#define PPDS_FUNCTION_{{name}} int {{name}}_def({%- for arg in var_args -%}
{%- if arg.type is defined -%}
{{arg.type}} {{arg}}
{%- elif arg.ptype is defined -%}
{{arg}}_expansion_for_func_def
{%- endif -%}
{{ ", " if not loop.last else "" }}
{%- endfor -%}
)


// declaration
PPDS_FUNCTION_{{name}};

*/


/* PPDS_DEF:
*/

/* PPDS_UNDEF:
*/

/* PPDS_PY_WRAPPER:
# prepare every argument here
{% for arg in var_args %}
# {{arg.__dict__}} # this is just # {'_value': 'ARR', 'ptype': 'ARR1D'} # sadly
# want something like the following:
# ptr = np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags="C_CONTIGUOUS", shape=(3,))
# len = ctypes.c_int
{{arg}}_ = definition_of_{{arg}} # hier das richtige erzeugen dann
{% endfor %}
_lib.{{name}}_def.argtypes = [{% for arg in var_args %}{{arg}}_, {% endfor %}]
def {{name}}({%- for arg in var_args -%}{{arg}}{{", " if not loop.last else ""}}{%- endfor -%}):
    return _lib.{{name}}_def({%- for arg in var_args -%}{{arg}}{{", " if not loop.last else ""}}{%- endfor -%})
*/


#define PPDS_DECLARE_FUNCTION_NEW(name, ...) PPDS_FUNCTION_##name



