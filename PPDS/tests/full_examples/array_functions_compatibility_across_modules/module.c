//
// Created by julian on 6/8/23.
//

#include "module.h"
#include "PPDS_SOURCE_ARR1D.h"
#include "PPDS_SOURCE_FUNCTION_NEW.h"

#include "PPDS_DEF_module.h"

PPDS_DECLARE_ARR1D(A, p : type(int *), n : type(const int))
PPDS_SOURCE_FUNCTION_NEW(get_value, A : ptype(ARR1D), ind : type(int), out : type(int *)) {
    if (ind < n and ind >= 0) {
        &out = A(i);
        return 0;
    }
    return 1;
}

#include "PPDS_UNDEF_module.h"
