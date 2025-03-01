#include <stdio.h>
#include <ctype.h>

// Define a cross-platform secure input function
#ifdef _MSC_VER  
    #define SCANF scanf_s
#else 
    #define SCANF scanf
#endif

void performOperation(char option);

int main() {
    char option;
    int validInput = 0;

    puts("Welcome to the Math Practice Program! \n");
    printf(" Developed By jewgra1002\n ");

    while (!validInput) {
        printf("\nChoose an operation:\n");
        printf("A - Addition\nS - Subtraction\nM - Multiplication\nD - Division\n");
        printf("Enter your choice: ");

        if (SCANF(" %c", &option, 1) != 1) {  // Uses scanf_s() for MSVC, scanf() for others
            while (getchar() != '\n'); // Clear input buffer
            printf("Invalid input. Please enter A, S, M, or D.\n");
            continue;
        }

        option = toupper(option);

        if (option == 'A' || option == 'S' || option == 'M' || option == 'D') {
            validInput = 1;
        } else {
            printf("Invalid choice. Please enter A, S, M, or D.\n");
        }
    }

    performOperation(option);
    return 0;
}

void performOperation(char option) {
    float num1, num2, result;

    printf("Enter two numbers: ");
    if (SCANF("%f %f", &num1, &num2) != 2) {
        printf("Invalid numbers entered.\n");
        return;
    }

    switch (option) {
        case 'A':
            result = num1 + num2;
            printf("Result: %.2f + %.2f = %.2f\n", num1, num2, result);
            break;
        case 'S':
            result = num1 - num2;
            printf("Result: %.2f - %.2f = %.2f\n", num1, num2, result);
            break;
        case 'M':
            result = num1 * num2;
            printf("Result: %.2f * %.2f = %.2f\n", num1, num2, result);
            break;
        case 'D':
            if (num2 != 0) {
                result = num1 / num2;
                printf("Result: %.2f / %.2f = %.2f\n", num1, num2, result);
            } else {
                printf("Error: Division by zero is not allowed.\n");
            }
            break;
    }
}