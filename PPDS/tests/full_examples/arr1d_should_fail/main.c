
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "PPDS_SOURCE_ARR1D.h"

#include "PPDS_DEF_1.h"
int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    assert(x!=NULL);
    int i;
    for (i=0; i<n; i++) {
        x[i] = i;
    }

    PPDS_DECLARE_ARR1D(X, x, n);

    printf("%d", X(n));

    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"
