#define _POSIX_C_SOURCE 2
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>

#include "send2py.h"

#include "PPDS_SOURCE_ARR1D.h"

#include "PPDS_DEF_1.h"
int main() {

    printf("in start of main.\n");
    const int n = 1000;
    double *x = (double*)malloc(n*sizeof(double));
    assert(x!=NULL);
    for (int i=0; i<n; i++) {
        x[i] = (i*0.1-10)*(i*0.1-30);
    }

    PPDS_DECLARE_ARR1D(X,x,n);

    init_pipe();

    const char * msg = "START_CALL;foo;2;END_CALL;FINISH;";
    int err = str_to_py(msg,strlen(msg));
    if (err != 0) {
        printf("str_to_py exited with %d ", err);
        return 1;
    }


    err = close_pipe();
    if (err != 0) {
        printf("close_pipe exited with %d ", err);
        return 1;
    }


    free(x); x=NULL;
    return 0;
}
#include "PPDS_UNDEF_1.h"
