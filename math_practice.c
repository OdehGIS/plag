#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Global variables for statistics
float ttlProblems = 0, ttlCorrect = 0;

// Function prototypes
int addition();
int subtraction();
int multiplication();
int division();

int main() {
    // Character array for the program title
    char title[] = "John Doe's Math Program Practice Main Menu"; // Replace "John Doe" with your name
    puts(title);

    int choice;
    do {
        // Display the main menu
        printf("\n1. Addition\n");
        printf("2. Subtraction\n");
        printf("3. Multiplication\n");
        printf("4. Division\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                ttlCorrect += addition();
                ttlProblems++;
                break;
            case 2:
                ttlCorrect += subtraction();
                ttlProblems++;
                break;
            case 3:
                ttlCorrect += multiplication();
                ttlProblems++;
                break;
            case 4:
                ttlCorrect += division();
                ttlProblems++;
                break;
            case 5:
                printf("\nExiting the program...\n");
                break;
            default:
                printf("\nInvalid choice! Please try again.\n");
        }
    } while (choice != 5);

    // Display statistics
    if (ttlProblems > 0) {
        float percentCorrect = (ttlCorrect / ttlProblems) * 100;
        printf("\nTotal Problems Attempted: %.0f\n", ttlProblems);
        printf("Total Correct Answers: %.0f\n", ttlCorrect);
        printf("Percentage Correct: %.2f%%\n", percentCorrect);
    } else {
        printf("\nNo problems were attempted.\n");
    }

    return 0;
}

// Addition function
int addition() {
    srand(time(0));
    int num1 = rand() % 100;
    int num2 = rand() % 100;
    int answer;

    printf("\nWhat is %d + %d? ", num1, num2);
    scanf("%d", &answer);

    if (answer == num1 + num2) {
        printf("Correct!\n");
        return 1;
    } else {
        printf("Incorrect. The correct answer is %d.\n", num1 + num2);
        return 0;
    }
}

// Subtraction function
int subtraction() {
    srand(time(0));
    int num1 = rand() % 100;
    int num2 = rand() % 100;
    int answer;

    printf("\nWhat is %d - %d? ", num1, num2);
    scanf("%d", &answer);

    if (answer == num1 - num2) {
        printf("Correct!\n");
        return 1;
    } else {
        printf("Incorrect. The correct answer is %d.\n", num1 - num2);
        return 0;
    }
}

// Multiplication function
int multiplication() {
    srand(time(0));
    int num1 = rand() % 20;
    int num2 = rand() % 20;
    int answer;

    printf("\nWhat is %d * %d? ", num1, num2);
    scanf("%d", &answer);

    if (answer == num1 * num2) {
        printf("Correct!\n");
        return 1;
    } else {
        printf("Incorrect. The correct answer is %d.\n", num1 * num2);
        return 0;
    }
}

// Division function
int division() {
    srand(time(0));
    int num1 = rand() % 100 + 1;
    int num2 = rand() % 10 + 1;
    int answer;

    printf("\nWhat is %d / %d? (Enter the quotient) ", num1, num2);
    scanf("%d", &answer);

    if (answer == num1 / num2) {
        printf("Correct!\n");
        return 1;
    } else {
        printf("Incorrect. The correct answer is %d.\n", num1 / num2);
        return 0;
    }
}
