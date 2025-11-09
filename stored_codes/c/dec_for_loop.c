#include <stdio.h>

int main(){
    for (int i = 15; i>=0; i--){
        if(i==5){
            break; // Exit the loop when i is 5
        }
        printf("The value of i is %d\n", i); // Prints values from 15 to 6  
    }
    return 0;
}