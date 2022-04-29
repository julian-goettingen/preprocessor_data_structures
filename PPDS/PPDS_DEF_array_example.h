// AUTOGENERATED, DO NOT EDIT.
// This file was created by PPDS.

// This file contains definitions generated by DECLARE statements.


// public:
#define X(i, j) x[X_assert_in_bounds(i,j,#i,#j), i*nx + j]


// internal:
#if (0) != 0

#define X_assert_with_index(expr,msg, idx_val, idx_name) ((void)0)
#define X_assert_in_bounds(i,j) ((void)0)

#else //skip_checks

#define X_assert_in_bounds(i,j,iname, jname) \
	X_assert_with_index((i)>=0, iname "<0 is out of bounds for axis 0 of size nx=nx", i, iname), \
	X_assert_with_index((i)<nx, iname ">=nx is out of bounds for axis 0 of size nx=nx", i, iname), \
	X_assert_with_index((j)>=0, jname "<0 is out of bounds for axis 1 of size ny=ny", j, jname), \
	X_assert_with_index((j)<ny, jname ">=ny is out of bounds for axis 1 of size ny=ny", j, jname)

#define X_assert_with_index(expr,msg, idx_val, idx_name) (void)(expr?(void)0:(X_assert_fail_with_index(expr,msg, idx_val, idx_name)))

#endif //skip_checks


#define X_assert_fail_with_index(expr,msg,idx_val,idx_name) \
	fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE: %s <----\n", msg),\
	fprintf(stderr, "index " idx_name " has value "), PRINT(idx_val),\
	fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
	fprintf(stderr, "with the object X declared in file: array_example.c, line 12 of type ARR2D\n"),\
	fprintf(stderr, "object X defined by: pointer=x, nx=nx, ny=ny\n"),\
	fprintf(stderr, "values of X:\n"), PRINT(x), PRINT(nx), PRINT(ny),\
	PRINT_ARR(x,nx*ny),\
	fprintf(stderr, #expr " evaluated to %d, exiting program.\n", expr),\
	exit(1)


