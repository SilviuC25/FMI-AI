#pragma once
#ifndef VEHICLE_H
#define VEHICLE_H

#include <iostream>
#include <string>

class Vehicle {
protected:
    std::string model;
    int year;
    double dailyRate;

public:
    Vehicle(std::string modelValue, int yearValue, double dailyRateValue);
    std::string getModel();
    int getYear();
    double getDailyRate();
    void setDailyRate(double newDailyRate);
    virtual void display() const;
};

#endif