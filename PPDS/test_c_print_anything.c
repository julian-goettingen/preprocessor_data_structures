#include "c11_print_anything.h"
#include<stdlib.h>

#define ZSIZE 50

int main() {

    const int N = 2;
    PRINT(N);
    printf("\n");

    int x[] = {1,2,3};
    PRINT_ARR(x,3);

    long z[ZSIZE] = {-1,789789,8,900,0};
    PRINT_ARR(z,ZSIZE);

    unsigned long zu[ZSIZE] = {1,789789,8,900,0};
    PRINT_ARR(zu,ZSIZE);

    
    printf("\n");
    size_t s = 100;
    PRINT(s);
    printf("\n");
    
    int ny = 50;
    float * y = malloc(sizeof(double)*ny);
    y[10] = 5;
    PRINT_ARR(y,ny);
    printf("\n");
    PRINT_ARR((y+1),40);
    printf("\n");
    PRINT(y[0]);
}
