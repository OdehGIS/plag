#include <stdio.h>

#define MAX_SIZE 10

int main() {
    char data[MAX_SIZE];
    int result;
    
    printf(" Developed By jewgra1002\n ");

    puts("Enter your string (no spaces, max 9 characters):");
    
    result = scanf("%9s", data); // Use scanf safely with width specifier

    if (result == 1) {
        puts("You entered:");
        puts(data);
    } else {
        printf("Your string is too large for the array size.\n");
    }

    return 0;
}
