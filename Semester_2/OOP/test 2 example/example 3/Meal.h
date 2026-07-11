#pragma once
#ifndef MEAL_H
#define MEAL_H
#include "Ingredient.h"
#include <string>
#include <vector>

class Meal : public Ingredient {
private:
    std::vector<Ingredient> ingredients;
public:
    Meal(std::string name, std::vector<Ingredient> ingredients);
    void addIngredient(Ingredient ing);
    void addMeal(Meal meal);
    int getCalories() const override;
    int getProtein() const override;
    int getCarbo() const override;
    int getFat() const override;
    int getFiber() const override;
};

#endif