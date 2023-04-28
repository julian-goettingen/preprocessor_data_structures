
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
{
  "args": ["name", "pointer", "len"],
  "kwargs": {"skip_checks": "NDEBUG", "numpy_wraparound": "0", "panic": "exit(1)", "print_element":"PRINT", "print_idx":"PRINT", "print_base":"PRINT"}
}
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

*/

/* PPDS_UNDEF:
#undef {{name}}_WRAP
#undef {{name}}_assert_fail
#undef {{name}}_assert_in_bounds
#undef {{name}}
*/


// this is declared so weirdly because "..." in the c-preprocessor means "1 or more arguments"
#define PPDS_DECLARE_ARR1D(name, pointer, /*len,*/ ...) ((void)0);

/*
#if {{numpy_wraparound}}
#define {{name}}_WRAP(i) (i < 0 ? ({{len}} + i) : i)
#else
#define {{name}}_WRAP(i) i
#endif

#if {{skip_checks}}
#define {{name}}_assert_in_bounds(i, expr_name) ((void)0)
#else

#   if {{numpy_wraparound}}

#define {{name}}_assert_in_bounds(i, expr_name) ((((i) >= {{len}}) || ((i) < -({{len}}))) ? (void){{name}}_assert_fail(i, expr_name) : ((void)0))

#   else //numpy_wraparound

#define {{name}}_assert_in_bounds(i, expr_name) ((((i) >= {{len}}) || ((i) < 0) )? (void){{name}}_assert_fail(i, expr_name) : ((void)0))

#   endif //numpywraparound

#endif //skip_checks

#define {{name}}_assert_fail(i, expr_name) \
	fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE: index of 1D-Array is OUT OF BOUNDS <----\n"),\
  fprintf(stderr,"index " expr_name " is out of bounds for ARR1D of size "), PRINT({{len}}),\
  fprintf(stderr, "numpywraparound is {{numpy_wraparound}}.\n"),\
	fprintf(stderr,"\ndetected in line %d, function %s, file %s\n",__LINE__,__func__,__FILE__),\
	fprintf(stderr, "with the object {{name}} declared in {{declare_site}} of type ARR1D\n"),\
	fprintf(stderr, "object {{name}} defined by: pointer={{pointer}}, len={{len}} numpy_wraparound={{numpy_wraparound}}\n"),\
	fprintf(stderr, "values of {{name}}:\n"), PRINT({{pointer}}), {{print_idx}}({{len}}),\
  PRINT_ARR({{pointer}}, {{len}}),\
  fprintf(stderr, " calling panic action: {{panic}}\n"),\
  (void){{panic}} */
