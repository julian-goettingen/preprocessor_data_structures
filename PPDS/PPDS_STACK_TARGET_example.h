




#define X_assert(expr,msg) (void)(expr?(void)0:(X_assert_fail(expr,msg)))


#define X_PUSH(elem) do{ x[X_assert(X_size<N,"max size reached, cant push more items"), X_size++] = (elem);}while(0)

#define X_POP() x[X_assert(X_size>0,"cant pop from empty stack"), --X_size]

#define X_AT(i) x[X_assert(i>=0 && i<X_size,"i=" #i "is out of bounds for the stack of size " X_size), X_size]

#define X_assert_fail(expr,msg) \
    fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE with the object X (declared in file: example.c, line 17)\n"),\
    fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
    fprintf(stderr, "object X defined by: size=X_size, maxsize=N, pointer=x\n"),\
    fprintf(stderr, "hex dumps of values in preprocessor-object X:\n"), ERRPRINT_WILD(X_size), ERRPRINT_WILD(x), ERRPRINT_WILD(N),\
    fprintf(stderr,msg),\
    fprintf(stderr,"\n" #expr " evaluated to %d, exiting program.\n", expr),\
    exit(1)







#define Y_assert(expr,msg) (void)(expr?(void)0:(Y_assert_fail(expr,msg)))


#define Y_PUSH(elem) do{ y[Y_assert(Y_size<M,"max size reached, cant push more items"), Y_size++] = (elem);}while(0)

#define Y_POP() y[Y_assert(Y_size>0,"cant pop from empty stack"), --Y_size]

#define Y_AT(i) y[Y_assert(i>=0 && i<Y_size,"i=" #i "is out of bounds for the stack of size " Y_size), Y_size]

#define Y_assert_fail(expr,msg) \
    fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE with the object Y (declared in file: example.c, line 28)\n"),\
    fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
    fprintf(stderr, "object Y defined by: size=Y_size, maxsize=M, pointer=y\n"),\
    fprintf(stderr, "hex dumps of values in preprocessor-object Y:\n"), ERRPRINT_WILD(Y_size), ERRPRINT_WILD(y), ERRPRINT_WILD(M),\
    fprintf(stderr,msg),\
    fprintf(stderr,"\n" #expr " evaluated to %d, exiting program.\n", expr),\
    exit(1)


