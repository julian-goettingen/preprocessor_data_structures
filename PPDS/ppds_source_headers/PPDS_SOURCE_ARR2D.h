#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
{
"args": ["name", "pointer", "nx", "ny"],
"kwargs": {"skip_checks": "NDEBUG", "numpy_wraparound": 0, "panic": "exit(1)"}
}
*/

/*  PPDS_DEF:

///////////////////////////////////
// FROM: {{declare_site}}
///////////////////////////////////


// public:

{% import 'macros.jinja2' as util -%}

#define {{name}}(i, j) {{pointer}}[{{name}}_assert_in_bounds(i,j,#i,#j), {{name}}_WRAP_Dim0(i)*{{ny}} + {{name}}_WRAP_Dim1(j)]

// internal:

{{ util.define_dim_helpers(name, nx, 'Dim0', numpy_wraparound, skip_checks) }}
{{ util.define_dim_helpers(name, ny, 'Dim1', numpy_wraparound, skip_checks) }}


{{util.define_assert_fail(name, "ARR2D", numpy_wraparound, declare_site, panic)}}

#define {{name}}_assert_in_bounds(i,j,i_string,j_string) {{name}}_assert_in_bounds_of_Dim0(i,i_string), {{name}}_assert_in_bounds_of_Dim1(j,j_string)

*/


/* PPDS_UNDEF:

///////////////////////////////////
// FDASD HIER KORRIGIEREN!!!, VERWEIS AUF HEADER-SOURCEW
// FROM: {{declare_site}}
///////////////////////////////////


#undef {{name}}_WRAP
#undef {{name}}_assert_with_index
#undef {{name}}_assert_fail_with_index
#undef {{name}}_assert_in_bounds
#undef {{name}}
*/


// this is declared so weirdly because ... in the c-preprocessor means "1 or more arguments"
#define PPDS_DECLARE_ARR2D(name, pointer, nx, /*ny,*/ ...) ((void)0);


