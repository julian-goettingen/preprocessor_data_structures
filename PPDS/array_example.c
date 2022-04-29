#include <stdlib.h>
#include <stdio.h>
#include "PPDS_SOURCE_ARR2D.h"


#include "PPDS_DEF_array_example.h"

int main(){
	const int nx = 3;
	const int ny = 40;

	int * x = (int*)calloc(nx*ny, sizeof(int));
	PPDS_DECLARE_ARR2D(X, x, nx, ny, skip_checks=0);


	printf("%d\n", X(0,0));
	printf("%d\n", X(2,3));
	printf("%d\n", X(0,39));


	for (int i=0; i<nx; i++){
		for (int j=0; j<ny; j++){
			X(i,j) = i;
		}
	}

	printf("%d\n", X(2,39));

}


#include "PPDS_UNDEF_array_example.h"
