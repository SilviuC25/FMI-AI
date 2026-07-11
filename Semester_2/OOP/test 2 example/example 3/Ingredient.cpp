#include <iostream>
#include <string>
#include "Ingredient.h"

using namespace std;

ostream& operator<<(ostream& os, Ingredient& ing) {
    os << "Ingredient: "  << ing.name << " with serving size of " << ing.quantity << " grams has " << ing.calories << " calories, "
        << ing.protein << " prortein, " << ing.carbo << " carbohydrates, " << ing.fat << " fats and " << ing.fiber << " fibers.";
    return os;
}

Ingredient::Ingredient(string name, int quantity, int calories, int protein, int carbo, int fat, int fiber) :
    name(name), quantity(quantity), calories(calories), protein(protein), carbo(carbo), fat(fat), fiber(fiber) {}

string Ingredient::getName() {
    return name;
}

int Ingredient::getQuantity() const {
    return quantity;
}

int Ingredient::getCalories() const {
    return calories;
}

int Ingredient::getProtein() const {
    return protein;
}

int Ingredient::getCarbo() const {
    return carbo;
}

int Ingredient::getFat() const {
    return fat;
}

int Ingredient::getFiber() const {
    return fiber;
}
