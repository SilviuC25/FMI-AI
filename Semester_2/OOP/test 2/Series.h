#pragma once

#include <string>
#include <iostream>
#include <vector>
#include "LibraryItem.h"
#include "Volume.h"

class Series : public LibraryItem {
private:
    std::vector<Volume> volumes;

public:
    Series(std::string title, float price, float worldbuildingQuality);
    std::string getTitle();
    std::vector<Volume> getVolumes();
    virtual void display() const override;
    void addVolume(Volume volume);
    float getSeriesPrice();
    float getSeriesQuality();
};
