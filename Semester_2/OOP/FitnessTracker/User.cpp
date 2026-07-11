#include "User.h"
#include <algorithm>
#include <stdexcept>

User::User(const std::string& id, const std::string& name)
    : userId(id), name(name) {}

std::string User::getId() const { return userId; }
std::string User::getName() const { return name; }

void User::addActivity(std::shared_ptr<Activity> activity) {
    for (const auto& act : activities) {
        if (act->getId() == activity->getId()) {
            throw std::runtime_error("Activity ID already exists for this user.");
        }
    }
    activities.push_back(activity);
}

void User::removeActivity(const std::string& activityId) {
    auto it = std::remove_if(activities.begin(), activities.end(),
                             [&activityId](const std::shared_ptr<Activity>& act) {
                                 return act->getId() == activityId;
                             });

    if (it == activities.end()) {
        throw std::runtime_error("Activity not found for this user.");
    }
    activities.erase(it, activities.end());
}

std::vector<std::shared_ptr<Activity>> User::getActivities() const {
    return activities;
}
