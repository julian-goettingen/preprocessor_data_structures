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



/* PPDS_DEF:

// a 'function call' is actually this macro expansion
#define {{name}} {{name}}_def

// for the function declaration/definition
#define PPDS_FUNCTION_{{name}} int {{name}}_def({% for arg in var_args %} {{arg.type}} {{arg}}{{ "," if not loop.last else "" }}{% endfor %})
*/

/* PPDS_UNDEF:
*/

#define PPDS_DECLARE_FUNCTION_NEW(name, ...) PPDS_FUNCTION_##name



