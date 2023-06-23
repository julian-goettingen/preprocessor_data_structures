
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

    PPDS_DECLARE_ARR1D(Xfull,x,n);
    PPDS_DECLARE_ARR1D(Xhalf,x,n/2);
    PPDS_DECLARE_ARR1D(Xother,(x+n/2),n/2);
    PPDS_DECLARE_ARR1D(Xwrap, x, n, numpy_wraparound=1);

    assert(Xfull(165) == 165);
    assert(Xhalf(10) == 10);
    assert(Xother(10) == 510);
    assert(Xwrap(-10) == 990);

    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"
