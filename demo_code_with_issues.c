/*
 * Sample C program with common issues for demonstration
 * This file demonstrates what the AI code analyzer can detect
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    // Issue 1: Uninitialized variable
    int x;
    
    // Issue 2: Unsafe buffer operations
    char buffer[100];
    gets(buffer);  // Unsafe - can cause buffer overflow
    
    // Issue 3: Format string vulnerability
    printf(buffer);  // Should be printf("%s", buffer)
    
    // Issue 4: Unsafe string copy
    char dest[50];
    strcpy(dest, buffer);  // No bounds checking
    
    // Issue 5: Memory leak
    char *dynamic = malloc(1000);
    strcpy(dynamic, "Hello, World!");
    printf("%s\n", dynamic);
    // Missing free(dynamic)
    
    // Issue 6: Magic number
    int array[500];  // Should use a named constant
    
    // Issue 7: scanf without bounds
    scanf("%s", dest);  // Can overflow dest buffer
    
    return 0;
}
