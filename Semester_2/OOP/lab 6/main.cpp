#include "vehicle.h"

int main() {
    Garage myGarage;

    myGarage.addVehicle(new Car("B-123-ABC", "Sedan"));
    myGarage.addVehicle(new Truck("B-999-XYZ", 15.5));
    myGarage.addVehicle(new Car("B-555-WOW", "Hatchback"));

    myGarage.display();

    return 0;
}