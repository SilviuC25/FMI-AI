#include <iostream>
#include <string>
#include <vector>
#include "Ingredient.h"
#include "Meal.h"

using namespace std;

Meal::Meal(string name, vector<Ingredient> initialIngredients) : Ingredient(name, 0, 0, 0, 0, 0, 0) {
    this->ingredients = initialIngredients;
}

int Meal::getCalories() const {
    int total = 0;
    for (auto& ing : ingredients) {
        total += ing.getCalories();
    }
    return total;
}

int Meal::getProtein() const {
    int total = 0;
    for (auto& ing : ingredients) {
        total += ing.getProtein();
    }
    return total;
}

int Meal::getCarbo() const {
    int total = 0;
    for (auto& ing : ingredients) {
        total += ing.getCarbo();
    }
    return total;
}

int Meal::getFat() const {
    int total = 0;
    for (auto& ing : ingredients) {
        total += ing.getFat();
    }
    return total;
}

int Meal::getFiber() const {
    int total = 0;
    for (auto& ing : ingredients) {
        total += ing.getFiber();
    }
    return total;
}

