#pragma once
#ifndef CAR_H
#define CAR_H

#include "Vehicle.h"
#include <string>

class Car : public Vehicle {
private:
    int seats;
    std::string fuelType;

public:
    int getSeats();
    std::string getFuelType();
    Car(std::string modelValue, int yearValue, double dailyRateValue, int seatsValue, std::string fuelTypeValue);
    virtual void display() const override;
};

#endif