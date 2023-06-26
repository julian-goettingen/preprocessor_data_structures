#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
args:
    - name
    - pointer
    - nx
    - ny
kwargs:
    skip_checks: NDEBUG
    numpy_wraparound: "0"
    panic: exit(1)
*/

/* PPDS_CONSTRUCTORS:
[
    "\\s*PPDS_DECLARE_ARR2D(\\(.*)",
    "\\s*PPDS_FN_ARG_ARR2D(\\(.*)"
]
 */

/*  PPDS_DEF:

///////////////////////////////////
// FROM: {{declare_site}}
///////////////////////////////////


// public:

{% import 'macros.jinja2' as util -%}

#define {{name}}(i, j) {{pointer}}[{{name}}_assert_in_bounds((i),(j),#i,#j), {{name}}_WRAP_Dim0((i))*{{ny}} + {{name}}_WRAP_Dim1((j))]

#define {{name}}_nx {{nx}}
#define {{name}}_ny {{ny}}

// internal:

{{ util.define_dim_helpers(name, nx, 'Dim0', numpy_wraparound, skip_checks) }}
{{ util.define_dim_helpers(name, ny, 'Dim1', numpy_wraparound, skip_checks) }}


{{util.define_assert_fail(name, "ARR2D", numpy_wraparound, declare_site, panic)}}

#define {{name}}_assert_in_bounds(i,j,i_string,j_string) {{name}}_assert_in_bounds_of_Dim0(i,i_string), {{name}}_assert_in_bounds_of_Dim1(j,j_string)

*/


/* PPDS_UNDEF:

///////////////////////////////////
// FROM: {{declare_site}}
///////////////////////////////////


#undef {{name}}_WRAP
#undef {{name}}_assert_with_index
#undef {{name}}_assert_fail_with_index
#undef {{name}}_assert_in_bounds
#undef {{name}}
#undef {{name}}_nx
#undef {{name}}_ny
*/

/* PPDS_DEFS_FOR_HEADER:
#define {{name}}_expand_for_call(X) X_pointer, X_nx, X_ny
{% if pointer.type is defined and nx.type is defined and ny.type is defined %}
#define {{name}}_expansion_for_func_def {{pointer.type}} {{pointer}}, {{nx.type}} {{nx}}, {{ny.type}} {{ny}}
{% else %}
#define {{name}}_expansion_for_func_def "to use ARR2D {{name}} (from {{declare_site}}) in definitions, annotate the type of nx, ny and underlying datastructure. Example: PPDS_DECLARE_ARR2D(X, p : type(int *), n1 : type(int), n2 : type(int) )"
{% endif %}
*/

// this is declared so weirdly because ... in the c-preprocessor means "1 or more arguments"
#define PPDS_DECLARE_ARR2D(name, pointer, nx, /*ny,*/ ...) ((void)0);


