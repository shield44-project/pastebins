#include <stdio.h>

int main(){
    int i=5;
    int *j=&i;
    int **k=&j;
// ***&&&a =a cancels out
    printf("The value of i is %d\n", **k); // i *j *(&i) **k ***w **(&j) .....
    printf("The value of i is %d\n", **(&j));
    return 0;
}

//FUctions calls
/*
1. Call by value: sending values of arguments
2. call by reference: sending the address of arguments

*/