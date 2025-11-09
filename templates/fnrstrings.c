#include <stdio.h>
#include <string.h>

int main(){
    char st[]="Harry";
    char a1[56]="Harry";
    char a2[56]="Bhai-";
    printf("%u",st);
    // printf("%ld",strlen(st)); // excluding null chr
    char target[30];
    strcpy(target,st);
    // printf("%s %s",st,target);
    strcat(a1,a2); // a1 now contains harrybhai
    printf("%s %s",a1,a2);
    int a=strcmp("far","ajoke"); // give positibe if ajoke comes first acc to dictironary and gives negative value if the far comes first 
    printf("%d",a);
    return 0;
}