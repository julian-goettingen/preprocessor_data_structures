#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#include "PPDS_SOURCE_FUNCTION_NEW.h"

#include "PPDS_DEF_1.h"


PPDS_DECLARE_FUNCTION_NEW(sum, a : type(int), b : type(int)) {
    return 1;
}


int main() {

    if (sum(1,2) != 1) {
        return 1;
    }

    return 0;
}

#include "PPDS_UNDEF_1.h"
