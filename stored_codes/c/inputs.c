#include <stdio.h>

int main(){
    char st[4]; 
    scanf("%s",st); // or &st[0] scanf add null already so no need of \n cant use multiword or spcases string must  big enough to fit it 
    printf("%s",st);
    return 0;
}