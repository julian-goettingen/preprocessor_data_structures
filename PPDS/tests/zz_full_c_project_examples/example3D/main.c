
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "PPDS_SOURCE_ARR3D.h"

#include "PPDS_DEF_1.h"
int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    assert(x!=NULL);
    for (int i=0; i<n; i++) {
        x[i] = 0;
    }


    PPDS_DECLARE_ARR3D(X,x,10,10,10);

    X(0,0,3) = 3;
    X(0,2,0) = 2;
    X(1,0,0) = 1;
    X(7,3,4) = 777;

    // with a 10x10x10 array, linear indices are easy to calculate
    assert(x[3] == 3);
    assert(x[20] == 2);
    assert(x[100] == 1);
    assert(x[734] == 777);

    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"
