#pragma once
#ifndef DIETARYGOAL_H
#define DIETARYGOAL_H
#include "WeeklyTracker.h"

class DietaryGoal {
private:

public:
    virtual bool isMet(WeeklyTracker& tracker) const = 0;
    DietaryGoal() {}
};

class CalorieGoal : public DietaryGoal {
private:
    int minCalories;
    int maxCalories;
public:
    CalorieGoal(int minCalories, int maxCalories) : DietaryGoal(), minCalories(minCalories), maxCalories(maxCalories) {}
    bool isMet(WeeklyTracker& tracker) const override {
        if (tracker.totalCalories() >= minCalories && tracker.totalCalories() <= maxCalories) {
            return true;
        }
        return false;
    }
};

class ProteinGoal : public DietaryGoal {
private:
    int minProtein;
public:
    ProteinGoal(int minProtein) : DietaryGoal(), minProtein(minProtein) {}
    bool isMet(WeeklyTracker& tracker) const override {
        return tracker.totalProtein() >= minProtein;
    }
};

class CarbLimit : public DietaryGoal {
private:
    int maxCarbo;
public:
    CarbLimit(int maxCarbo) : DietaryGoal(), maxCarbo(maxCarbo) {}
    bool isMet(WeeklyTracker& tracker) const override {
        return tracker.totalCarbo() <= maxCarbo;
    }
};



#endif