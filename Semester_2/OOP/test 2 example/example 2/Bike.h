#pragma once 
#ifndef BIKE_H
#define BIKE_H

#include "Vehicle.h"
#include <string>

class Bike : public Vehicle {
private:
    std::string bikeType;

public:
    std::string getBikeType();
    Bike(std::string modelValue, int yearValue, double dailyRateValue, std::string bikeTypeValue);
    virtual void display() const override;
};

#endif