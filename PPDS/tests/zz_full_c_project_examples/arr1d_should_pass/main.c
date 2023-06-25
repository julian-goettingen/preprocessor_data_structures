
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

    PPDS_DECLARE_ARR1D(X,x,n,numpy_wraparound=1);

    printf("%d %d %d %d %d %d", X(0), X(-1), X(1), X(n-1), X(-2), X(-3));fflush(stdout);
    assert(X(-1) == n-1);
    assert(X(-3) == n-3);

    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"
