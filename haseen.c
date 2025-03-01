#include <stdio.h>

// Function to calculate final total with tax
float calculateTotal(float totalSales) {
    return totalSales + (totalSales * 0.06);
}

int main() {
    // Welcome message using character array
    printf(" Developed By jewgra1002\n ");
    char welcomeMessage[] = "Welcome to Hansen's Discount Supermarket!"; 
    puts(welcomeMessage);

    // Declaring  variables
    int numItems;
    float prices[100]; 
    float totalSales = 0.0, finalTotal;

    // Ask user for number of items
    printf("Enter the number of items to total: ");
    scanf("%d", &numItems);

    // Get prices from user
    for (int i = 0; i < numItems; i++) {
        do {
            printf("Enter price of item %d: ", i + 1);
            scanf("%f", &prices[i]);

            if (prices[i] > 10.00) {
                printf("Invalid price! Please enter a price below $10.00.\n");
            }
        } while (prices[i] > 10.00);

        totalSales += prices[i];
    }

    // Calculate final total with tax
    finalTotal = calculateTotal(totalSales);

    // Display results
    printf("\nTotal Sales: $%.2f\n", totalSales);
    printf("Sales Tax (6%%): $%.2f\n", totalSales * 0.06);
    printf("Final Total: $%.2f\n", finalTotal);

    return 0;
}
