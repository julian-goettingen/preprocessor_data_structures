#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
{
"args": ["name", "pointer", "nx", "ny", "nz"],
"kwargs": {"skip_checks": "NDEBUG", "numpy_wraparound": 0, "panic": "exit(1)"}
}
*/


/* PPDS_CONSTRUCTORS:
[
    "\\s*PPDS_DECLARE_ARR3D(\\(.*)",
    "\\s*PPDS_FN_ARG_ARR3D(\\(.*)"
]
 */

/*  PPDS_DEF:

///////////////////////////////////
// FROM: {{declare_site}}
///////////////////////////////////


// public:

{% import 'macros.jinja2' as util -%}

#define {{name}}(i, j, k) {{pointer}}[{{name}}_assert_in_bounds(i,j,k,#i,#j,#k), {{name}}_WRAP_Dim2(i)*{{nz}}*{{ny}} + {{name}}_WRAP_Dim1(j)*{{nz}} + {{name}}_WRAP_Dim2(k)]

// internal:

{{ util.define_dim_helpers(name, nx, 'Dim0', numpy_wraparound, skip_checks) }}
{{ util.define_dim_helpers(name, ny, 'Dim1', numpy_wraparound, skip_checks) }}
{{ util.define_dim_helpers(name, nz, 'Dim2', numpy_wraparound, skip_checks) }}


{{util.define_assert_fail(name, "ARR3D", numpy_wraparound, declare_site, panic)}}

#define {{name}}_assert_in_bounds(i,j,k,i_string,j_string,k_string) {{name}}_assert_in_bounds_of_Dim0(i,i_string), {{name}}_assert_in_bounds_of_Dim1(j,j_string), {{name}}_assert_in_bounds_of_Dim2(k, k_string)

*/


/* PPDS_UNDEF:

///////////////////////////////////
// FROM: {{declare_site}}
///////////////////////////////////

{% import 'macros.jinja2' as util -%}

{{ util.undef_dim_helpers(name, 'Dim0')}}
{{ util.undef_dim_helpers(name, 'Dim1')}}
{{ util.undef_dim_helpers(name, 'Dim2')}}

{{ util.undef_assert_fail(name) }}

#undef {{name}}_assert_in_bounds
#undef {{name}}

*/


// this is declared so weirdly because ... in the c-preprocessor means "1 or more arguments"
#define PPDS_DECLARE_ARR3D(name, pointer, nx, ny, /*nz,*/ ...) ((void)0);


