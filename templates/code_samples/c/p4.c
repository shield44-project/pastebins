#include <stdio.h>

void npia(int a[],int n){
    int no_of_positive=0;
    for(int i=0;i<n;i++){
        if(a[i]>0){
            no_of_positive ++; //int temp[]={a[i]};
        }
    }
    printf("The number of positive integers in the given array is %d ", no_of_positive);
}
int main()
{
    int array[] = {-1, -2, -3, -4, -5, -6, -7, -8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    npia(array,19);
    return 0;
}