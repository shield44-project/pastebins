#include <stdio.h>

int main(){
    int j=45;
    int* k=&j;// k is a pouner pointing to j
    int metaman=99;
    int x=10000;
    int* beta=&x;
    printf("%p\n",&x);
    printf("%d\n",*(&x));
    printf("%u\n",*beta);
    printf("%u\n",&j);
    printf("%p\n",&k);// Every variable has its address 
    printf("The address of %d is %p in hexadecimals\n",j,&j);
    // printf("%u in hexadecimals\n",j,&j);
    printf("\nThe Address is %p\n",k);
    printf("%p",&metaman);
    printf("\nThe value of address j is %d\n",*(&j));
    printf("\nThe value of address j is %d",*k);
    return 0;
}