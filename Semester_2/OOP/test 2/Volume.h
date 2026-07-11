#pragma once

#include <string>
#include <iostream>
#include "LibraryItem.h"


class Volume : public LibraryItem {
private:
    int publicationYear;
public:
    Volume(std::string title, float price, float worldbuildingQuality, int publicationYear);
    virtual void display() const override;
    
};
