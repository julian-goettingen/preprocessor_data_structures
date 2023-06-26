//
// Created by julian on 6/8/23.
//

#include "module.h"
#include "PPDS_SOURCE_ARR1D.h"
#include "PPDS_SOURCE_ARR2D.h"
#include "PPDS_SOURCE_FUNCTION_NEW.h"

#include "PPDS_DEF_module.h"

PPDS_DECLARE_ARR1D(ARR, p : type(int *), n : type(const int));
PPDS_SOURCE_FUNCTION_NEW(get_value, ARR : ptype(ARR1D), ind : type(int), out : type(int *)) {
    if (ind < n  && ind >= 0) {
        &out = ARR(i);
        return 0;
    }
    return 1;
}

PPDS_DECLARE_ARR2D(OUT, p: type(int *), nx : type(const int), ny : type(const int));
PPDS_DECLARE_ARR1D(A, P: type(int *), len_a : type(const int));
PPDS_DECLARE_ARR1D(B, P: type(int *), len_b : type(const int));
PPDS_SOURCE_FUNCTION_NEW(outer, OUT: ptype(ARR2D), A: ptype(ARR1D), B: ptype(ARR1D)) {
    for (int i=0; i<A_len; i++) {
        for (int j=0; j<B_len; j++) {
        }
    }
}

#include "PPDS_UNDEF_module.h"
