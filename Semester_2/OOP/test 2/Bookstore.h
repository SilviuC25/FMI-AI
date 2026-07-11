#pragma once

#include <iostream>
#include <string>
#include <vector>
#include "Series.h"
#include "Volume.h"
#include "LibraryItem.h"
using namespace std;

class Bookstore {
private:
    vector<LibraryItem> items;

public:
    Bookstore();
    void addItem(LibraryItem item);
    void displayQualityItems(float minQuality);
    virtual void display();
};
