#include <stdio.h>

int s(int *,int *);

// Sum should change value of a
int s(int* x, int* y){
    *x=6;
    return *x+*y;
}
int main(){
    int a=1,b=2;
    s(&a,&b); //
    printf("The value of a is %d",a);
    return 0;
}