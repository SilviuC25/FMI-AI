#include "Activity.h"

Activity::Activity(const std::string& id, const std::string& type, int duration, int calories, const std::string& date)
    : id(id), type(type), duration(duration), caloriesBurned(calories), date(date) {}

std::string Activity::getId() const { return id; }
std::string Activity::getType() const { return type; }
int Activity::getDuration() const { return duration; }
int Activity::getCaloriesBurned() const { return caloriesBurned; }
std::string Activity::getDate() const { return date; }

void Activity::setType(const std::string& type) { this->type = type; }
void Activity::setDuration(int duration) { this->duration = duration; }
void Activity::setCaloriesBurned(int calories) { this->caloriesBurned = calories; }
void Activity::setDate(const std::string& date) { this->date = date; }
