#pragma once;
#ifndef RENTALAGENCY_H
#define RENTALAGENCY_H

#include "Car.h"
#include "Vehicle.h"
#include "Bike.h"
#include <vector>


class RentalAgency {
private:
    std::vector<Vehicle*> vehicles;

public:
    virtual void display() const;
    void addVehicle();
};
#endif