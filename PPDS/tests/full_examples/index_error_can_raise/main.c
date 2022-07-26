
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include <stdexcept>

#include "PPDS_SOURCE_ARR1D.h"

#include "PPDS_DEF_1.h"

void throw_bad_index() {
    throw std::invalid_argument("bad index");
}

int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    assert(x!=NULL);
    for (int i=0; i<n; i++) {
        x[i] = i;
    }

#if __cplusplus
    PPDS_DECLARE_ARR1D(X,x,500,panic=throw_bad_index());
    try {
        X(900) = 5;
    } catch(std::invalid_argument& e) {
        fprintf(stderr, "Caught exception\n");
        assert(x[900] == 900); // make sure the array-access was prevented.
    }
#endif

    free(x); x=NULL;
    return 0;
}
#include "PPDS_UNDEF_1.h"
