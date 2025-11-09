#include <stdio.h>

void display();

int main(){
    int a; // void means returns nothing variable declaration
    display(); // Fn call
    return 0;
}

// Fn definition
void display(){
    printf("hi i am a display\n");
}