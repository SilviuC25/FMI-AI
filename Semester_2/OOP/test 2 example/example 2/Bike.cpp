#include <iostream>
#include <string>

#include "Vehicle.h"
#include "Bike.h"

using namespace std;

Bike::Bike(string modelValue, int yearValue, double dailyRateValue, string bikeTypeValue)
    : Vehicle(modelValue, yearValue, dailyRateValue) {
        bikeType = bikeTypeValue;
    }

string Bike::getBikeType() {
    return bikeType;
}

void Bike::display() const {
    Vehicle::display();
    cout << " | Bike Type: " << bikeType;
}

