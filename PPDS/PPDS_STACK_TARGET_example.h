




#define X_assert(expr,msg) (void)(expr?(void)0:(X_assert_fail(expr,msg)))


#define X_PUSH(elem) do{ x[X_assert(X_size<N,"max size reached, cant push more items"), X_size++] = (elem);}while(0)

#define X_POP() x[X_assert(X_size>0,"cant pop from empty stack"), --X_size]

#define X_AT(i) x[X_assert(i>=0 && i<X_size,"i=" #i "is out of bounds for the stack of size " X_size), X_size]

#define X_assert_fail(expr,msg) \
    fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE: %s <----\n", msg),\
    fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
    fprintf(stderr, "with the object X declared in file: example.c, line 18 of type STACK\n"),\
    fprintf(stderr, "object X defined by: size=X_size, maxsize=N, pointer=x\n"),\
    fprintf(stderr, "values of X:\n"), PRINT(X_size), PRINT(x), PRINT(N),\
    PRINT_ARR(x,X_size),\
    fprintf(stderr, #expr " evaluated to %d, exiting program.\n", expr),\
    exit(1)







#define Y_assert(expr,msg) (void)(expr?(void)0:(Y_assert_fail(expr,msg)))


#define Y_PUSH(elem) do{ y[Y_assert(Y_size<M,"max size reached, cant push more items"), Y_size++] = (elem);}while(0)

#define Y_POP() y[Y_assert(Y_size>0,"cant pop from empty stack"), --Y_size]

#define Y_AT(i) y[Y_assert(i>=0 && i<Y_size,"i=" #i "is out of bounds for the stack of size " Y_size), Y_size]

#define Y_assert_fail(expr,msg) \
    fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE: %s <----\n", msg),\
    fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
    fprintf(stderr, "with the object Y declared in file: example.c, line 29 of type STACK\n"),\
    fprintf(stderr, "object Y defined by: size=Y_size, maxsize=M, pointer=y\n"),\
    fprintf(stderr, "values of Y:\n"), PRINT(Y_size), PRINT(y), PRINT(M),\
    PRINT_ARR(y,Y_size),\
    fprintf(stderr, #expr " evaluated to %d, exiting program.\n", expr),\
    exit(1)


