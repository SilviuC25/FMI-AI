#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <stdexcept>
#include <algorithm>

class Device {
private:
    std::string model;
public:
    Device(std::string m) : model(m) {}
    virtual ~Device() {}
    virtual void turnOn() const {
        std::cout << "Device " << model << " is starting up...\n";
    }
};

class Smartphone : public Device {
    double* batteryHealth;
public:
    Smartphone(std::string m, double health) : Device(m) {
        batteryHealth = new double(health);
    }
    ~Smartphone() override {
        delete batteryHealth;
    }
    void turnOn() const override {
        std::cout << "Smartphone screen lights up. Battery health: " << *batteryHealth << "%\n";
    }
};

template <typename T>
void bootDevice(const T& dev) {
    dev.turnOn();
}

void processingCenter() {
    Smartphone phone("Galaxy S26", 98.5);
    throw std::out_of_range("Voltage overload!");
    std::cout << "Processing completed normally.\n";
}

int main() {
    // Section 1
    Device basic("OldNokia");
    Smartphone smart("iPhone 17", 94.2);
    
    bootDevice(basic);
    bootDevice(smart);

    // Section 2
    std::vector<std::shared_ptr<Device>> inventory;
    inventory.push_back(std::make_shared<Smartphone>("Pixel 10", 89.0));
    inventory.push_back(std::make_shared<Device>("GenericRouter"));

    for (const auto& item : inventory) {
        item->turnOn();
    }

    // Section 3
    try {
        processingCenter();
    } 
    catch (const std::exception& e) {
        std::cout << "Exception caught: " << e.what() << "\n";
    }
    catch (const std::out_of_range& err) {
        std::cout << "Out of range caught: " << err.what() << "\n";
    }

    return 0;
}