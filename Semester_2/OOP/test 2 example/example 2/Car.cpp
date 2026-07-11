#include <iostream>
#include <string>

#include "Vehicle.h"
#include "Car.h"

using namespace std;

int Car::getSeats() {
    return seats;
}

string Car::getFuelType() {
    return fuelType;
}

Car::Car(string modelValue, int yearValue, double dailyRateValue, int seatsValue, string fuelTypeValue)
    : Vehicle(modelValue, yearValue, dailyRateValue) {
        seats = seatsValue;
        fuelType = fuelTypeValue;

        if (seatsValue > 10) {
            throw runtime_error("Number of seats is not valid");
        }
    }

void Car::display() const {
    Vehicle::display();
    cout << " | Seats: " << seats << " | Fuel Type: " << fuelType;
}
