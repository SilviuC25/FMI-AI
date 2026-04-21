#include <stdio.h>
#include <stdlib.h>

int maxTripletValue(int* arr, unsigned int n, int* first, int* second, int* third) {
  if (n < 3) {
    printf("The array has less than 3 elements. Application will now stop.");
    return 0;
  }
  
  int maxValue = -1e9;

  for (unsigned int i = 0; i < n; ++i) {
    for (unsigned int j = 0; j < n; ++j) {
      for (unsigned int k = 0; k < n; ++k) {
        if (i != j && i != k && j != k) {
          int a = arr[i], b = arr[j], c = arr[k];
          int value  = a * b * c;
          if (value >= maxValue) {
            maxValue = value;

            *first = a, *second = b, *third = c;

            if (*first > *second) { 
              int temp = *first; 
              *first = *second; 
              *second = temp; 
            }
            if (*second > *third) { 
              int temp = *second; 
              *second = *third; 
              *third = temp; 
            }
            if (*first > *second) { 
              int temp = *first; 
              *first = *second; 
              *second = temp; 
            }

          }
        }
      }
    }
  return maxValue;
  }
}

int main() {
  unsigned int n;
  printf("Enter the size of the array: ");
  scanf("%u", &n);

  int *arr = (int*) malloc(sizeof(int) * n); 
  if (!arr) { 
    printf("Failed to allocate memory! App will now stop\n"); 
    exit(-1); 
  }

  printf("Enter the numbers: ");

  for (unsigned int i = 0; i < n; ++i) {
    scanf("%d", &arr[i]);
    arr[i] = arr[i];
  }

  // printf("The numbers are: "); 
  // for (unsigned int i = 0; i < n; i++) 
  //   printf("%d ", arr[i] ); 

  int firstVal = 0, secondVal = 0, thirdVal = 0;
  int *first = &firstVal, *second = &secondVal, *third = &thirdVal;

  int maxValue = maxTripletValue(arr, n, first, second, third);

  firstVal = *first, secondVal = *second, thirdVal = *third;

  if (n < 3) {
    return 0;
  }

  printf("The maximum triplet is: (%d, %d, %d), with a maximum product of %d\n", firstVal, secondVal, thirdVal, maxValue);

  return 0;
}

/*
example: 
5
-3 10 200 4 -900
*/