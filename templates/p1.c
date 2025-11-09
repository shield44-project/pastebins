#include <stdio.h>

int avg(int,int,int);

int avg(int x,int y,int z){
    return (x+y+z)/3;
}
int main(){
    int n1,n2,n3;
    printf("Enter Number 1:");
    scanf("%d",&n1);
    printf("Enter Number 2:");
    scanf("%d",&n2);
    printf("Enter Number 3:");
    scanf("%d",&n3);
    printf("Average of these 3 numbers is %d", avg(n1,n2,n3));
    return 0;
}