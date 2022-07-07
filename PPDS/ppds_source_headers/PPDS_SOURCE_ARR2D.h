#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
{
"args": ["name", "pointer", "nx", "ny"],
"kwargs": {"skip_checks": "NDEBUG", "numpy_wraparound": 0}
}
*/

/*  PPDS_DEF:

///////////////////////////////////
// FROM: {{declare_site}}
///////////////////////////////////


// internal:

#if {{numpy_wraparound}} //numpy_wraparound
#define {{name}}_WRAP(i,dimlen) ((i < 0 ? dimlen + i) : i)
#else //numpy_wraparound
#define {{name}}_WRAP(i,dimlen) i
#endif //numpy_wraparound

#if {{skip_checks}} != 0 // skip_checks

#define {{name}}_assert_with_index(expr,msg, idx_val, idx_name, dim_val, dim_name) ((void)0)
#define {{name}}_assert_in_bounds(i,j,iname, jname) ((void)0)

#else //skip_checks is zero, so do the checks

#define {{name}}_assert_ind_small_enough(i,j,iname,jname) \
	{{name}}_assert_with_index((i)<{{nx}}, iname ">=nx is OUT OF BOUNDS for axis 0 of size nx={{nx}}", i, iname, {{nx}}), \
	{{name}}_assert_with_index((j)<{{ny}}, jname ">=ny is OUT OF BOUNDS for axis 1 of size ny={{ny}}", j, jname, {{ny}})


#	if {{numpy_wraparound}} // numpy_wraparound

#define {{name}}_assert_in_bounds(i,j,iname, jname) \
	{{name}}_assert_ind_small_enough(i,j,iname,jname), \
	{{name}}_assert_with_index((i)>=(-nx), iname "<(-nx) is OUT OF BOUNDS for axis 0 of size nx={{nx}}", i, iname, {{nx}}), \
	{{name}}_assert_with_index((j)>=0, jname "<0 is OUT OF BOUNDS for axis 1 of size ny={{ny}}", j, jname, {{ny}}) \

#	else //numpy_wraparound

#define {{name}}_assert_in_bounds(i,j,iname, jname) \
	{{name}}_assert_ind_small_enough(i,j,iname,jname), \
	{{name}}_assert_with_index((i)>=0, iname "<0 is OUT OF BOUNDS for axis 0 of size nx={{nx}}", i, iname, {{nx}}), \
	{{name}}_assert_with_index((j)>=0, jname "<0 is OUT OF BOUNDS for axis 1 of size ny={{ny}}", j, jname, {{ny}}) \

#	endif //numpy_wraparound

#define {{name}}_assert_with_index(expr,msg, idx_val, idx_name, dim) (void)(expr?(void)0:({{name}}_assert_fail_with_index(expr,msg, idx_val, idx_name, dim, #dim)))

#endif //skip_checks


#define {{name}}_assert_fail_with_index(expr,msg,idx_val,idx_name, dim_val, dim_name) \
	fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE: %s <----\n", msg),\
	fprintf(stderr, "index " idx_name " has value "), PRINT(idx_val), \
	fprintf(stderr, " in dimension " dim_name " of size "), PRINT(dim_val),\
	fprintf(stderr,"\ndetected in line %d, function %s, file %s\n",__LINE__,__func__,__FILE__),\
	fprintf(stderr, "with the object {{name}} declared in {{declare_site}} of type ARR2D\n"),\
	fprintf(stderr, "object {{name}} defined by: pointer={{pointer}}, nx={{nx}}, ny={{ny}}\n"),\
	fprintf(stderr, "values of {{name}}:\n"), PRINT({{pointer}}), PRINT({{nx}}), PRINT({{ny}}),\
	PRINT_ARR({{pointer}},{{nx}}*{{ny}}),\
	fprintf(stderr, #expr " evaluated to %d, exiting program.\n", expr),\
	exit(1)




// public:

#define {{name}}(i, j) {{pointer}}[{{name}}_assert_in_bounds(i,j,#i,#j), {{name}}_WRAP(i,{{nx}})*{{ny}} + {{name}}_WRAP(j,{{ny}})]

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

#define PPDS_DECLARE_ARR2D(name, pointer, nx, ny, ...) ((void)0);
