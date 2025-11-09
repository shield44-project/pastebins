#include <stdio.h>

void printArray(int a[],int n){
    for(int i=0;i<n;i++){
        printf("%d",a[i]);
    }
    printf("\n");
}

void reverse(int arr[],int n){
    int temp;
    for (int i=0;i<n/2;i++){
        temp=arr[i];
        arr[i]=arr[n-i-1];
        arr[n-i-1]=temp;
    }
}
int main(){
    int arr[]={1,2,3,4,5,6};
    printArray(arr,6);
    reverse(arr,6);
    printArray(arr,6);
    return 0;
}

// temp=a a=b b=temp
// 0 to 5 
// 1 to 4 and 2 to 3
// i from 0 to n/2
// arr[i] to arr[n-i-1]