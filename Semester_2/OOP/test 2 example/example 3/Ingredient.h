#pragma once
#ifndef INGREDIENT_H
#define INGREDIENT_H
#include <string>

class Ingredient {
private:
    std::string name;
    int quantity;
    int calories;
    int protein;
    int carbo;
    int fat;
    int fiber;

public:
    Ingredient(std::string name, int quantity, int calories, int protein, int carbo, int fat, int fiber);
    std::string getName();
    virtual int getQuantity() const;
    virtual int getCalories() const;
    virtual int getProtein() const;
    virtual int getCarbo() const;
    virtual int getFat() const;
    virtual int getFiber() const;
    friend std::ostream& operator<<(std::ostream& os, Ingredient& ing);
};

#endif