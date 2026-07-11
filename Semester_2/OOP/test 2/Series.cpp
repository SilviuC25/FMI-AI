#include <iostream>
#include <string>
#include <vector>
#include "Volume.h"
#include "Series.h"
#include "LibraryItem.h"

using namespace std;

Series::Series(string title, float price, float worldbuildingQuality) : LibraryItem(title, price, worldbuildingQuality) {
    title = title;
    price = getSeriesPrice();
    worldbuildingQuality = getSeriesQuality();
}

string Series::getTitle() {
    return title;
}

vector<Volume> Series::getVolumes() {
    return volumes;
}

void Series::display() const {
    cout << "The title is: " << title << "\n";
    // for (auto& v : getVolumes()) {
    //     v.display();
    //     cout << "\n";
    // }
}

void Series::addVolume(Volume volume) {
    if (this->getVolumes().size() > 2) {
        throw length_error("Cannot add more than 3 volumes to the Series.");
    }
    volumes.push_back(volume);
}

float Series::getSeriesPrice() {
    float total = 0.0;
    int cnt = 0;
    // for (auto& v : getVolumes()) {
    //     ++cnt;
    //     total += v.getPrice();
    // }
    if (cnt == 3) {
        total = (float)0.8 * total;
    }
    return total;
}

float Series::getSeriesQuality() {
    float total = 0, cnt = 0;
    // for (auto& v : getVolumes()) {
    //     total += v.getPrice();
    //     ++cnt;
    // }
    return (float)total / cnt;
}


