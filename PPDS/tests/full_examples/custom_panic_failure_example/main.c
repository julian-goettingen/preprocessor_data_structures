
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "PPDS_SOURCE_ARR1D.h"

void set_to_1(int *var) {
  *var = 1;
}

#include "PPDS_DEF_1.h"
int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    assert(x!=NULL);
    for (int i=0; i<n; i++) {
        x[i] = i;
    }

    int err = 0;
    PPDS_DECLARE_ARR1D(X,x,(n-10),panic=set_to_1(&err));

    // going out of bounds on this sets the error-variable to 1
    // NOTE: the array-access is still being resolved if the panic-action does not prevent it with an exit or an exception (or, I guess, a longjump)
    // this might cause undefined behaviour
    // if the requested index is out of bounds on the underlying data structure

    // safe and recommended way is to exit on fail

    printf("%d\n", X(n-5));

    free(x); x=NULL;


    // this is for integration with the test-pipeline
    if (err==1) {
      return -1;
    }
}
#include "PPDS_UNDEF_1.h"
