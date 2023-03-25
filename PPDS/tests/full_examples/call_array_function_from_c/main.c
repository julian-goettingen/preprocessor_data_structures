#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#include "PPDS_SOURCE_FUNCTION.h"

#include "PPDS_DEF_1.h"
//
//PPDS_FUNCTION(hello_world, const char *hello_world()) {
//    return "HELLO";
//}
//
//PPDS_FUNCTION(check_not_seven, const char *check_not_seven(int x)) {
//    if (x == 7) {
//        return "it is seven";
//    }
//    return NULL;
//}
//
//PPDS_FUNCTION(check_sum_is_not_seven, const char *check_sum_is_not_seven(double a, int x, const int z)) {
//    if (a+x+z == 7.0) {
//        return "it is seven";
//    }
//    return NULL;
//}
//
//PPDS_FUNCTION(compute_on_arr, const char *compute_on_arr(ARR1D(A, double *x, size_t n))) {
//    for (int i=0; i<n; i++) {
//        A(i) = i;
//    }
//    return NULL;
//}
//


int main() {

//    if (hello_world()== NULL) {
//        fprintf(stderr, "should have returned HELLO");
//        return 1;
//    }
//    if (check_not_seven(8) != NULL) {
//        fprintf(stderr, "should have signalled success (with a null)");
//        return 2;
//    }
//    if (check_not_seven(7) == NULL) {
//        fprintf(stderr, "should have signalled error, arg is 7");
//        return 3;
//    }
//    if (check_sum_is_not_seven(2,3.0,11) != NULL) {
//        fprintf(stderr, "should have signalled success (with a null)");
//        return 4;
//    }
//    if (check_sum_is_not_seven(2,2.0,3) == NULL) {
//        fprintf(stderr, "should have signalled error, sum is 7");
//        return 5;
//    }




    return 0;
}

#include "PPDS_UNDEF_1.h"
