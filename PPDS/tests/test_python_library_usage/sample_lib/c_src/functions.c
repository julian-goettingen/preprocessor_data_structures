#include<stdio.h>

#include "functions.h"

#include "PPDS_SOURCE_ARR1D.h"
#include "PPDS_SOURCE_FUNCTION_NEW.h"

#include "PPDS_DEF_1.h"

PPDS_DECLARE_FUNCTION_NEW(hello_int, num : type(int)) {
    printf("Hello %d!\n", num);
    return 0;
}

#include "PPDS_UNDEF_1.h"


