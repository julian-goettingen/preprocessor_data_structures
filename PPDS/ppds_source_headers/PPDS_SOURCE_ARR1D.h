#ifndef PPDS_SOURCE_ARR1D_H
#define PPDS_SOURCE_ARR1D_H
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
args:
    - name
    - pointer
    - len
kwargs:
    skip_checks: NDEBUG
    numpy_wraparound: "0"
    panic: exit(1)
    print_element: PRINT
    print_idx: PRINT
    print_base: PRINT
*/

/* PPDS_CONSTRUCTORS:
[
    "\\s*PPDS_DECLARE_ARR1D(\\(.*)",
    "\\s*PPDS_FN_ARG_ARR1D(\\(.*)"
]
 */

/* PPDS_DEF:
{% import 'macros.jinja2' as util -%}

// public:
#define {{name}}(i) {{pointer}}[{{name}}_assert_in_bounds(i), {{name}}_WRAP_len(i)]

// internal:

{{ util.define_dim_helpers(name, len, 'len', numpy_wraparound, skip_checks) }}

#define {{name}}_assert_in_bounds(i) {{name}}_assert_in_bounds_of_len(i,#i)

{{util.define_assert_fail(name, "ARR1D", numpy_wraparound, declare_site, panic)}}


#define {{name}}_len {{len}}
#define {{name}}_pointer {{pointer}}

*/

/* PPDS_UNDEF:
#undef {{name}}_WRAP
#undef {{name}}_assert_fail
#undef {{name}}_assert_in_bounds
#undef {{name}}
#undef {{name}}_len
#undef {{name}}_pointer
*/

/* PPDS_DEFS_FOR_HEADER:
#define {{name}}_expand_for_call(X) X_pointer, X_len
{% if pointer.type is defined and len.type is defined %}
#define {{name}}_expansion_for_func_def {{pointer.type}} {{pointer}}, {{len.type}} {{len}}
{% else %}
#define {{name}}_expansion_for_func_def "to use ARR1D {{name}} (from {{declare_site}}) in definitions, annotate the type of the length and underlying datastructure. Example: PPDS_DECLARE_ARR1D(X, p : type(int *), n : type(int))"
{% endif %}
*/



// this is declared so weirdly because "..." in the c-preprocessor means "1 or more arguments"
#define PPDS_DECLARE_ARR1D(name, pointer, /*len,*/ ...)


#endif // PPDS_SOURCE_ARR1D_H
