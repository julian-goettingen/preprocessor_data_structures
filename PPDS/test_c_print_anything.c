#include "c_print_anything.h"
#include<stdlib.h>


int main() {

    const int N = 2;
    PRINT(N);
    printf("\n");

    int x[] = {1,2,3};
    PRINT_ARR(x,3);

    
    printf("\n");
    size_t s = 100;
    PRINT(s);
    printf("\n");
    
    double * y = malloc(sizeof(double)*5);
    PRINT_ARR(y,5);
    printf("\n");
    PRINT((y+1));
    printf("\n");
    PRINT(y[0]);
}
