#include <stdio.h>

#define NUM_SEATS 11 // Seats 1-10, ignore seat 0

// Function to check if a seat is available
int isSeatAvailable(int seatNumber, int seats[]) {
    if (seats[seatNumber] == 0) {
        return 1; // Seat is available
    }
    return 0; // Seat is not available
}

// Function to display available seats
void displayAvailableSeats(int seats[], int start, int end) {
    printf("\nAvailable seats: ");
    for (int i = start; i <= end; i++) {
        if (isSeatAvailable(i, seats)) {
            printf("%d ", i);
        }
    }
    printf("\n");
}

int main() {
    int seats[NUM_SEATS] = {0}; // Initialize all seats to 0 (empty)
    int seatsSold = 0; // Counter for sold seats
    int choice; // User's choice (1 for first-class, 2 for economy)
    int seatNumber; // Seat number chosen by the user
    int bookAnother; // Flag to check if the user wants to book another seat

    printf("Welcome to the Airline Seating Assignment Program!\n");

    while (seatsSold < 10) { // Loop until all seats are sold
        // Display menu options
        printf("\nPlease type 1 for \"first-class.\"\n");
        printf("Please type 2 for \"economy.\"\n");
        printf("Your choice: ");
        scanf("%d", &choice);

        if (choice == 1) { // First-class section (seats 1-5)
            displayAvailableSeats(seats, 1, 5); // Show available first-class seats
            printf("Enter the seat number you want to book: ");
            scanf("%d", &seatNumber);

            if (seatNumber >= 1 && seatNumber <= 5 && isSeatAvailable(seatNumber, seats)) {
                seats[seatNumber] = 1; // Mark seat as occupied
                seatsSold++;
                printf("\nBoarding Pass: Seat %d (First-Class)\n", seatNumber);
            } else {
                printf("\nInvalid seat number or seat already booked. Please try again.\n");
                continue; // Skip the rest of the loop and prompt again
            }
        } else if (choice == 2) { // Economy section (seats 6-10)
            displayAvailableSeats(seats, 6, 10); // Show available economy seats
            printf("Enter the seat number you want to book: ");
            scanf("%d", &seatNumber);

            if (seatNumber >= 6 && seatNumber <= 10 && isSeatAvailable(seatNumber, seats)) {
                seats[seatNumber] = 1; // Mark seat as occupied
                seatsSold++;
                printf("\nBoarding Pass: Seat %d (Economy)\n", seatNumber);
            } else {
                printf("\nInvalid seat number or seat already booked. Please try again.\n");
                continue; // Skip the rest of the loop and prompt again
            }
        } else {
            printf("\nInvalid choice. Please try again.\n");
            continue; // Skip the rest of the loop and prompt again
        }

        // Ask the user if they want to book another seat
        printf("\nWould you like to book another seat? (1 for Yes, 0 for No): ");
        scanf("%d", &bookAnother);

        if (bookAnother == 0) {
            printf("\nThank you for booking with us. Have a great flight!\n");
            break; // Exit the program if the user doesn't want to book another seat
        }

        if (seatsSold == 10) {
            printf("\nFlight is full.\n");
            break; // Exit the program if all seats are sold
        }
    }

    return 0;
}
