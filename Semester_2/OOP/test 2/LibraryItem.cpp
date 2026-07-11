#include <iostream>
#include <string>
#include "LibraryItem.h"
#include <stdexcept>

using namespace std;

LibraryItem::LibraryItem(string title, float price, float worldbuildingQuality) :
    title(title), price(price), worldbuildingQuality(worldbuildingQuality) {}

string LibraryItem::getTitle() {
    return title;
}

float LibraryItem::getPrice() {
    return price;
}

float LibraryItem::getWorldbuildingQuality() {
    return worldbuildingQuality;
}

void LibraryItem::setPrice(float newPrice) {
    price = newPrice;
}

void LibraryItem::setWorldbuildingQuality(float newWorldbuildingQuality) {
    if (newWorldbuildingQuality < 1 || newWorldbuildingQuality > 5) {
        throw invalid_argument("The rating should be a real number between 1 and 5.");
    }
    worldbuildingQuality = newWorldbuildingQuality;
}

void LibraryItem::display() const {
    cout << "The title is: " << title << ", the price is: " << price << " and the rating is: " << worldbuildingQuality << "\n";
}




