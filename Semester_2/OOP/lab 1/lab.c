#include <stdio.h>

int main(void) {
    char name[40];
    printf("Enter your name: ");
    scanf("%s39", name);
    printf("Hello, %s!\n", name);
    
    printf("Enter your birth year: ");
    int birthYear;
    int currentYear = 2026;
    scanf("%d", &birthYear);
    int age = currentYear - birthYear;
    printf("Your age is: %d\n", age);
    
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);
    int counter = 0;
    while (num) {
        if (num % 2) {
            counter = counter + 1;
        }
        num = num / 2;
    }
    printf("The number has %d 1's in its binary representation\n", counter);
    
    printf("The possible PIN codes of 4 digits with the sum 24 are: \n");
    int expectedSum = 24;
    
    for (int digit1 = 9; digit1 >= 0; --digit1) {
        for (int digit2 = 9; digit2 >= 0; --digit2) {
            for (int digit3 = 9; digit3 >= 0; --digit3) {
                for (int digit4 = 9; digit4 >= 0; --digit4) {
                    int currentSum = digit1 + digit2 + digit3 + digit4;
                    if (currentSum == expectedSum) {
                        printf("%d%d%d%d\n", digit1, digit2, digit3, digit4);
                    }
                 }
            }
        }
    }
    return 0;
}