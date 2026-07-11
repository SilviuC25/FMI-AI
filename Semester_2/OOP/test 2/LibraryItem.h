#pragma once

#include <string>
#include <iostream>

using namespace std;

class LibraryItem {
protected:
    std::string title;
    float price;
    float worldbuildingQuality;

public:
    LibraryItem(std::string title, float price, float worldbuildingQuality);
    std::string getTitle();
    float getPrice();
    float getWorldbuildingQuality();
    void setPrice(float newPrice);
    void setWorldbuildingQuality(float newWorldbuildingQuality);
    virtual void display() const;
};
