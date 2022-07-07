
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "PPDS_SOURCE_ARR1D.h"

#include "PPDS_DEF_1.h"
int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    assert(x!=NULL);
    for (int i=0; i<n; i++) {
        x[i] = i;
    }



    int error = 0;
    PPDS_DECLARE_ARR1D(X,x,n,panic= error=1 );
    
    printf("%d ", X(-1)); // this should set error to 1

    test failed weil der array-Zugriff illegale ist und deswegen output kommt
    und stderr output wird immer als fail gesehen.

    if (error == 0) {
        fprintf(stderr, "error was not set to 1");
        exit(1);
    }

    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"
