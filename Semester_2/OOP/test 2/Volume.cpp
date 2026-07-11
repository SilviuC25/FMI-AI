#include <iostream>
#include <string>
#include "LibraryItem.h"
#include "Volume.h"

using namespace std;

Volume::Volume(std::string title, float price, float worldbuildingQuality, int publicationYear) :
    LibraryItem(title, price, worldbuildingQuality), publicationYear(publicationYear) {}
    
void Volume::display() const {
    LibraryItem::display();
    cout << "Publication year is: " << publicationYear << "\n";
}

