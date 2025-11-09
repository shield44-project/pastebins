#include <stdio.h>

float ctof(float);

float ctof(float x){ // important thing
    return (9.0/5.0)*x+32;
}
int main(){
    float n;
    printf("Enter celsius value to convert it to fahreinheat: \n");
    scanf("%f",&n);
    printf("%0.2f F",ctof(n));
    return 0;
}