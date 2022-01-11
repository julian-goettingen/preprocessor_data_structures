#include "PPDS_STACK_SOURCE.h"
#include "PPDS_STACK_TARGET_example.h"
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>


int main(){
    int N = 10;
    int M = 20;

    // a comment

    int *x = (int*)malloc(sizeof(int)*N);
    assert(x);
    
    PPDS_DECLARE_STACK(X,x,N);
    X_PUSH(1);
    X_PUSH(2);
    X_PUSH(3);
    X_PUSH(4);
    for (int i=0; i<4; i++) {
        printf("%d, ", X_POP());
    }
    printf("\n");

    int y[M];
    PPDS_DECLARE_STACK(Y,y,M); 
    int a = Y_POP();
    (void) a;
    Y_PUSH(1);
    Y_PUSH(2);
    Y_PUSH(3);
    Y_PUSH(4);
    for (int i=0; i<4; i++) {
        printf("%d, ", Y_POP());
    }
    printf("\n");

    free(x); x=NULL; 

}
