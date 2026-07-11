#include <map>
#include <vector>
#include <vector>
#include "Ingredient.h"
#include "Meal.h"
#include "WeeklyTracker.h"
#include <stdexcept>

using namespace std;

bool WeeklyTracker::validDay(string day) {
    if (day == "Monday" || day == "Tuesday" || day == "Wednesday" || day == "Thursday" || day == "Friday" || day == "Saturday"
        || day == "Sunday") return true;
    return false;
} 

WeeklyTracker::WeeklyTracker() {}

void WeeklyTracker::addMealToDay(string day, Meal meal) {
    if (!validDay(day)) {
        throw runtime_error("Not a day of the week!");
    }
    consumedByDay[day].push_back(meal);
}

vector<Meal> WeeklyTracker::mealsByDay(string day) {
    return consumedByDay[day];
}

int WeeklyTracker::totalCalories() {
    int total = 0;
    for (auto entry : consumedByDay) {
        for (auto meal : entry.second) {
            total += meal.getCalories();
        }
    }
    return total;
}

int WeeklyTracker::totalProtein() {
    int total = 0;
    for (auto entry : consumedByDay) {
        for (auto meal : entry.second) {
            total += meal.getProtein();
        }
    }
    return total;
}

int WeeklyTracker::totalCarbo() {
    int total = 0;
    for (auto entry : consumedByDay) {
        for (auto meal : entry.second) {
            total += meal.getCarbo();
        }
    }
    return total;
}

int WeeklyTracker::totalFat() {
    int total = 0;
    for (auto entry : consumedByDay) {
        for (auto meal : entry.second) {
            total += meal.getFat();
        }
    }
    return total;
}

int WeeklyTracker::totalFiber() {
    int total = 0;
    for (auto entry : consumedByDay) {
        for (auto meal : entry.second) {
            total += meal.getFiber();
        }
    }
    return total;
}

string WeeklyTracker::maxProteinDay() {
    string day;
    int maxProtein = 0;
    for (auto entry : consumedByDay) {
        int protein = 0;
        for (auto meal : entry.second) {
            protein += meal.getProtein();
        }
        if (protein >= maxProtein) {
            day = entry.first;
        }
    }
    return day;
}