#ifndef ACTIVITY_H
#define ACTIVITY_H

#include <string>

class Activity {
private:
    std::string id;
    std::string type;
    int duration;
    int caloriesBurned;
    std::string date;

public:
    Activity() = default;
    Activity(const std::string& id, const std::string& type, int duration, int calories, const std::string& date);

    std::string getId() const;
    std::string getType() const;
    int getDuration() const;
    int getCaloriesBurned() const;
    std::string getDate() const;

    void setType(const std::string& type);
    void setDuration(int duration);
    void setCaloriesBurned(int calories);
    void setDate(const std::string& date);
};

#endif // ACTIVITY_H
