#include <stdio.h>

int main(){
    char st[30];
    gets(st); // for multiword the entered string gets stored in st
    printf("%s",st);
    // puts(st);
    printf("hey");
    return 0;
}

//gets is dangerous becuase of buffer overflow and deprecated