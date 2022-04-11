#include<stdlib.h>
#include<stdio.h>
#define VAR_MACRO(a1, a2, ...) printf("%d %d\n", a1, a2)


int main(){
	VAR_MACRO(1,2,"abc");
	VAR_MACRO(1,2,bounds=3);
}

