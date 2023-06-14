//
// Created by julian on 6/8/23.
//

#include "module.h"

PPDS_SOURCE_FUNCTION_NEW(get_value, A : ptype(ARR1D), ind : type(int), out : type(int *)) {
    if (ind < A_len and ind >= 0) {
        &out = A(i);
        return 0;
    }
    return 1;
}
