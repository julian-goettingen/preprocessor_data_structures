#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define FORCE_CXX_PRINT 1
//#define FORCE_CXX_PRINT
//#define FORCE_DUMP_PRINT
//#define AUTO_PRINT
#include "print_anything.h"


/* PPDS_ARGS:
{
"args": ["name", "pointer", "nx", "ny"],
"kwargs": {"skip_checks": "NDEBUG"}
}
*/

/* PPDS_DEF:

#if {{skip_checks}} != 0

#define {{name}}_assert_with_index(expr,msg, idx_val, idx_name) ((void)0)
#define {{name}}_assert_in_bounds(i,j) ((void)0)

#else //skip_checks

#define {{name}}_assert_in_bounds(i,j,iname, jname) \
	{{name}}_assert_with_index((i)>=0, iname "<0 is out of bounds for axis 0 of size nx={{nx}}", i, iname), \
	{{name}}_assert_with_index((i)<{{nx}}, iname ">=nx is out of bounds for axis 0 of size nx={{nx}}", i, iname), \
	{{name}}_assert_with_index((j)>=0, jname "<0 is out of bounds for axis 1 of size ny={{ny}}", j, jname), \
	{{name}}_assert_with_index((j)<{{ny}}, jname ">=ny is out of bounds for axis 1 of size ny={{ny}}", j, jname)

#define {{name}}_assert_with_index(expr,msg, idx_val, idx_name) (void)(expr?(void)0:({{name}}_assert_fail_with_index(expr,msg, idx_val, idx_name)))

#endif //skip_checks


#define {{name}}(i, j) {{pointer}}[{{name}}_assert_in_bounds(i,j,#i,#j), i*{{nx}} + j]

#define {{name}}_assert_fail_with_index(expr,msg,idx_val,idx_name) \
	fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE: %s <----\n", msg),\
	fprintf(stderr, "index " idx_name " has value "), PRINT(idx_val),\
	fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
	fprintf(stderr, "with the object {{name}} declared in {{declare_site}} of type ARR2D\n"),\
	fprintf(stderr, "object {{name}} defined by: pointer={{pointer}}, nx={{nx}}, ny={{ny}}\n"),\
	fprintf(stderr, "values of {{name}}:\n"), PRINT({{pointer}}), PRINT({{nx}}), PRINT({{ny}}),\
	PRINT_ARR({{pointer}},{{nx}}*{{ny}}),\
	fprintf(stderr, #expr " evaluated to %d, exiting program.\n", expr),\
	exit(1)

*/


/* PPDS_UNDEF:
#undef {{name}}_assert_with_index
#undef {{name}}_assert_fail_with_index
#undef {{name}}_assert_in_bounds
#undef {{name}}
*/

#define PPDS_DECLARE_ARR2D(name, pointer, nx, ny, ...) ((void)0);

