#include <iostream>
#include <string>
#include "Vehicle.h"

using namespace std;

string Vehicle::getModel() {
    return model;
}

int Vehicle::getYear() {
    return year;
}

double Vehicle::getDailyRate() {
    return dailyRate;
}

void Vehicle::setDailyRate(double newDailyRate) {
    if (newDailyRate < 10) {
        throw invalid_argument("Daily Rate value is not valid");
    }
    dailyRate = newDailyRate;
}

Vehicle::Vehicle(std::string modelValue, int yearValue, double dailyRateValue) 
    : model(modelValue), year(yearValue), dailyRate(dailyRateValue) {
        if (dailyRateValue < 10) {
            throw invalid_argument("Daily Rate value is not valid");
        }
    }

void Vehicle::display() const {
    cout << "Vehicle: " << model << " | Year: " << year << " | Daily Rate: " << dailyRate;
}