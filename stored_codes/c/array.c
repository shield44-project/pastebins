#include <stdio.h>

int main(){
    int marks[90]; // reserve space to store 90 integers in 90 elements 0 to 89
    marks[0]=95;
    marks[1]=90;
    // We can go alll the way till marks[89]
    printf("%d and %d", marks[0],marks[0]);
    return 0;
}