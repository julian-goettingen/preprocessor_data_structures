
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "PPDS_SOURCE_ARR1D.h"

#include "PPDS_DEF_2.h"
#include "PPDS_DEF_1.h"
int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    assert(x!=NULL);
    for (int i=0; i<n; i++) {
        x[i] = i;
    }

    PPDS_DECLARE_ARR1D(X,x,n);
    assert(X(3) == 3);


    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"
#include "PPDS_UNDEF_2.h"
