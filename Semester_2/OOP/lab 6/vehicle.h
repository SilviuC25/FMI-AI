#pragma once

#include <string>
#include <vector>

class Vehicle {
protected:
    std::string registrationNumber;

public:
    Vehicle(std::string registrationNumberValue);
    virtual ~Vehicle();
    virtual void display() = 0;
};

class Car : public Vehicle {
private:
    std::string bodyStyle;

public:
    Car(std::string registrationNumberValue, std::string bodyStyleValue);
    void setBodyStyle(std::string bodyStyleValue);
    std::string getBodyStyle();
    void display() override;
};

class Truck : public Vehicle {
private:
    double payloadCapacity;

public:
    Truck(std::string registrationNumberValue, double payloadCapacityValue);
    void setPayloadCapacity(double payloadCapacityValue);
    double getPayloadCapacity();
    void display() override;
};

class Garage {
private:
    std::vector<Vehicle*> vehicles;

public:
    ~Garage();
    void addVehicle(Vehicle* vehicleValue);
    void display();
};