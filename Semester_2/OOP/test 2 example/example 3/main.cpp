#include <bits/stdc++.h>
#include "DietaryGoal.h"
#include "WeeklyTracker.h"
#include "Meal.h"
#include "Ingredient.h"

using namespace std;

int main() {
    WeeklyTracker tracker;
    Ingredient egg("egg", 55, 80, 6, 0, 5, 0);
    Ingredient rice("rice", 100, 370, 6, 85, 1, 0);
    Ingredient chiken("chiken breast", 100, 120, 24, 0, 3, 0);
    Ingredient tuna("tuna", 100, 100, 18, 0, 4, 0);
    Ingredient oats("oat flakes", 100, 350, 7, 60, 5, 9);
    Ingredient vegMix("vegetable mix", 350, 300, 6, 60, 2, 11);
    Ingredient fruitMix("frozen fruit mix", 150, 90, 1, 20, 0, 4);
    vector<Ingredient> m1, m2, m3;
    m1.push_back(rice);
    m1.push_back(egg);
    m1.push_back(egg);
    m1.push_back(chiken);
    m2.push_back(rice);
    m2.push_back(tuna);
    m2.push_back(vegMix);
    m3.push_back(oats);
    m3.push_back(fruitMix);
    m3.push_back(egg);
    Meal meal1("Chiken Rice", m1), meal2("Tuna Rice", m2), meal3("Pancakes", m3);
    tracker.addMealToDay("Monday", meal1);
    tracker.addMealToDay("Monday", meal2);
    tracker.addMealToDay("Tuesday", meal3);
    tracker.addMealToDay("Sunday", meal1);
    tracker.addMealToDay("Sunday", meal3);

    try {
        tracker.addMealToDay("Today", meal2);
    } catch(std::runtime_error err) {
        cout << "The following error occured while adding a meal: " << err.what();
    }

    ProteinGoal proteinGoal(80);
    bool goal = proteinGoal.isMet(tracker);
    if (goal) {
        cout << "\nGoal was met";
    } else {
        cout << "\n Goal was not met";
    }

    string maxDay = tracker.maxProteinDay();    
    cout << "\n" << maxDay << "\n";
    return 0;
}