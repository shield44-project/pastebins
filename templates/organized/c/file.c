#include <stdio.h>

int main(){
    FILE *ptr;
    ptr=fopen("harry.txt","r");
    int num;
    fscanf(ptr,"%d",&num);
    printf("Value of num is %d\n",num);
    return 0;
}