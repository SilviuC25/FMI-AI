#ifndef USER_H
#define USER_H

#include <string>
#include <vector>
#include <memory>
#include "Activity.h"

class User {
private:
    std::string userId;
    std::string name;
    std::vector<std::shared_ptr<Activity>> activities;

public:
    User() = default;
    User(const std::string& id, const std::string& name);

    std::string getId() const;
    std::string getName() const;

    void addActivity(std::shared_ptr<Activity> activity);
    void removeActivity(const std::string& activityId);

    std::vector<std::shared_ptr<Activity>> getActivities() const;
};

#endif // USER_H
