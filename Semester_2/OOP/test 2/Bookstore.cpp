#include <iostream>
#include <string>
#include <vector>
#include "LibraryItem.h"
#include "Series.h"
#include "Bookstore.h"
#include "Volume.h"

using namespace std;

Bookstore::Bookstore() {}

void Bookstore::addItem(LibraryItem item) {
    items.push_back(item);
}

void Bookstore::displayQualityItems(float minQuality) {
    for (auto& item : this->items) {
        if (item.getWorldbuildingQuality() > minQuality) {
            item.display();
        }
    }
}

void Bookstore::display() {
    for (auto& item : this->items) {
        item.display();
    }
}