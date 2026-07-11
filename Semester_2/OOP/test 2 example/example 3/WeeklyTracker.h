#pragma once
#ifndef WEEKLYTRACKER_H
#define WEEKLYTRACKER_H

#include "Ingredient.h"
#include "Meal.h"
#include <string>
#include <vector>
#include <map>

class WeeklyTracker {
private:
    std::map<std::string, std::vector<Meal>> consumedByDay;
public:
    WeeklyTracker();
    std::vector<Meal> mealsByDay(std::string day);
    bool validDay(std::string);
    void addMealToDay(std::string day, Meal meal);
    int totalCalories();
    int totalProtein();
    int totalCarbo();
    int totalFat();
    int totalFiber();
    std::string maxProteinDay();
};

#endif