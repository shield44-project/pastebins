#include <stdio.h>

int main(){
    int marks[5];
    printf("Enter marks of 5 students\n");
    // scanf("%d",&marks[0]);
    // scanf("%d",&marks[1]);
    // scanf("%d",&marks[2]);
    // scanf("%d",&marks[3]);
    // scanf("%d",&marks[4]);
    for(int i=0;i<5;i++){
        scanf("%d",&marks[i]);
    }
     for(int i=0;i<5;i++){
        printf("The address of marks at index %d is %u\n",i,&marks[i]); // difference of 4 in each address of the blocks in arrays always like this u can change the pointer pointing element change elements by mem address +i ptr++ etc
     }
    return 0;
}