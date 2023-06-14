#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#include "PPDS_SOURCE_FUNCTION_NEW.h"
#include "PPDS_SOURCE_ARR1D.h"

#include "main_PPDS_GENERATED_DEFS_FOR_HEADER.h"

#include "PPDS_DEF_1.h"


PPDS_DECLARE_FUNCTION_NEW(sum, a : type(int), b : type(int)) {
    return a+b;
}

PPDS_DECLARE_ARR1D(X, x: type(int *), N: type(const int)); // at first lets to it with a 'global' definition

PPDS_DECLARE_FUNCTION_NEW(arr_sum, X: ptype(ARR1D), res: type(int *)) {
    *res = 0;
    for (int i=0; i<X_len; i++) {
        *res += X(i);
    }
    return 0;
}


int main() {

    if (sum(1,2) != 3) {
        return 1;
    }

    const int N = 100;
    int *x = (int*)malloc(sizeof(int)*N);
    for (int i=0; i<N; i++) {
        X(i) = i;
    }
    int res;
    int err = arr_sum(X, &res);
    if (err != 0){
        return 2;
    }
    if (res != (N*(N-1))/2) { // summing [0,N-1] yields this
        return 3;
    }

//     erster Wurf: kein compatibility-check, gar nichts, nur Macro expanden
//    need:
//    X_as_arg in 1D-array -> can use expansions to create it.
//    ptype-annotation -> really the best way?
//    1D-array expansion in the Function-header -> hmm, sollte aber die impl hier haben. Header definiert _impl-macro?
//    local functions should also be possible. -> do this first
//
//    die declaration sollte im header passieren, die Implementation hier
//    aber das mit den headern wäre noch eine Erweiterung
//
//
//    do not assume X is actually available at the site of the function!
//    in general it wont be.
//
//    the function and the callsite must use different ARR1D and a compatibility-check
//    the compatibility-check must be for the required-args, the others get passed?
//    Also es muss bei der Funktionsdefinition eine volle array-definition vorliegen.
//
//    Die muss da irgendwie reinkommen.
//
//    later:
//    the planned requiredType-annotation should be compatible with all of this
//
//
//    also:
//    function-defs should be written into a global scope to be importable elsewhere, not the local scope? maybe.



    return 0;
}

#include "PPDS_UNDEF_1.h"
