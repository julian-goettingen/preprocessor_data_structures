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


braucht Variable Zahl von Argumenten und muss die expansions benutzen können...

/* PPDS_DEF:

#define PPDS_FUNCTION_{{name}} int {{name}}({{var_args[0]}}, {{var_args[1]}})
*/

/* PPDS_UNDEF:
*/

#define PPDS_DECLARE_SOURCE_FUNCTION_NEW(name, __VAR_ARGS__) PPDS_FUNCTION_##name



