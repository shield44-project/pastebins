#include <stdio.h>

int main(){
    int marks[]={122,123,125,143};
    int *ptr=&marks[0]; // or use int *ptr =marks; for 1st elements 
    for (int i=0;i<4;i++){
        printf("The marks at %d is %d\n",i,marks[i]);
        printf("The marks at index %d is %d\n",i,*ptr);
        ptr++;
    }
    return 0;
}