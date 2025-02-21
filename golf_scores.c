#include <stdio.h>

// Function to compute the total score
int computeTotal(int scores[], int size) {
    int total = 0;
    for (int i = 0; i < size; i++) {
        total += scores[i]; // Accumulate the total score
    }
    return total;
}

int main() {
    int scores[9]; // Array to store scores for 9 holes
    int totalScore;

    printf("Welcome to the Golf Score Calculator!\n");

    // Input scores for all 9 holes
    for (int i = 0; i < 9; i++) {
        while (1) { // Loop until a valid score is entered
            printf("Enter score for hole %d (1-10): ", i + 1);
            scanf("%d", &scores[i]);
            if (scores[i] >= 1 && scores[i] <= 10) {
                break; // Exit the loop if the score is valid
            } else {
                printf("Invalid score! Please enter a score between 1 and 10.\n");
            }
        }
    }

    // Display scores for each hole
    printf("\nScores for each hole:\n");
    for (int i = 0; i < 9; i++) {
        printf("Hole %d: %d\n", i + 1, scores[i]);
    }

    // Compute and display the total score
    totalScore = computeTotal(scores, 9);
    printf("\nTotal Score: %d\n", totalScore);

    // Determine the golfer's performance
    if (totalScore >= 75) {
        printf("Excellent! You played an amazing game!\n");
    } else if (totalScore >= 50) {
        printf("Good! You played a solid game!\n");
    } else {
        printf("Better luck next time! Keep practicing!\n");
    }

    return 0;
}
