#include<stdio.h>

#include "functions.h"

#include "PPDS_SOURCE_ARR1D.h"
#include "PPDS_SOURCE_FUNCTION_NEW.h"

#include "PPDS_DEF_1.h"

PPDS_DECLARE_FUNCTION_NEW(hello_int, num : type(int)) {
    printf("Hello %d!\n", num);
    return 0;
}

PPDS_DECLARE_ARR1D(ARR, p: type(double *), n : type(int))
PPDS_DECLARE_FUNCTION_NEW(arr_sum, ARR: ptype(ARR1D)){
    int res = 0;
    printf("%d - ", n);
    for (int i=0; i<n; i++) {
        printf("%lf, ", ARR(i));
        res += ARR(i);
    }
    printf("\n");
    return res;
}

#include "PPDS_UNDEF_1.h"


