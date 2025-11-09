#include <stdio.h>

int change(int a);

int change(int a){
    a=44; // Misnomer
    return 0;
}

int main(){
    int b=22;
    int c;
    change(b); // b remains 22 it only gives copies
    printf("b is %d\n", b);
    return 0;
}