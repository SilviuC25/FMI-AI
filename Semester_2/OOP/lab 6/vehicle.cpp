#include "vehicle.h"
#include <iostream>

using namespace std;

Vehicle::Vehicle(string registrationNumberValue) {
    registrationNumber = registrationNumberValue;
}

Vehicle::~Vehicle() {}

Car::Car(string registrationNumberValue, string bodyStyleValue) 
    : Vehicle(registrationNumberValue) {
    bodyStyle = bodyStyleValue;
}

void Car::setBodyStyle(string bodyStyleValue) {
    bodyStyle = bodyStyleValue;
}

string Car::getBodyStyle() {
    return bodyStyle;
}

void Car::display() {
    cout << "Car Registration: " << registrationNumber << " | Style: " << bodyStyle << "\n";
}

Truck::Truck(string registrationNumberValue, double payloadCapacityValue) 
    : Vehicle(registrationNumberValue) {
    payloadCapacity = payloadCapacityValue;
}

void Truck::setPayloadCapacity(double payloadCapacityValue) {
    payloadCapacity = payloadCapacityValue;
}

double Truck::getPayloadCapacity() {
    return payloadCapacity;
}

void Truck::display() {
    cout << "Truck Registration: " << registrationNumber << " | Payload: " << payloadCapacity << " tons\n";
}

Garage::~Garage() {
    for (Vehicle* v : vehicles) {
        delete v;
    }
}

void Garage::addVehicle(Vehicle* vehicleValue) {
    vehicles.push_back(vehicleValue);
}

void Garage::display() {
    cout << "--- Garage Inventory ---\n";
    for (Vehicle* v : vehicles) {
        v->display();
    }
}