#include "Controller.h"
#include <stdexcept>

Controller::Controller(std::unique_ptr<BaseRepository> repository)
    : repo(std::move(repository)) {
    if (repo->getAllUsers().empty()) {
        User defaultUser("user1", "Alex");
        repo->addUser(defaultUser);
    }
    currentUserId = repo->getAllUsers()[0].getId();
}

void Controller::setCurrentUser(const std::string& userId) {
    currentUserId = userId;
    undoStack.clear();
    redoStack.clear();
}

std::string Controller::getCurrentUserId() const {
    return currentUserId;
}

void Controller::addUser(const std::string& id, const std::string& name) {
    User newUser(id, name);
    repo->addUser(newUser);
}

std::vector<User> Controller::getAllUsers() const {
    return repo->getAllUsers();
}

void Controller::addActivityToCurrentUser(const std::string& id, const std::string& type, int duration, int calories, const std::string& date) {
    auto activity = std::make_shared<Activity>(id, type, duration, calories, date);
    auto cmd = std::make_unique<AddActivityCommand>(*repo, currentUserId, activity);
    cmd->execute();
    undoStack.push_back(std::move(cmd));
    redoStack.clear();
}

void Controller::removeActivityFromCurrentUser(const std::string& activityId) {
    User& user = repo->getUserById(currentUserId);
    std::shared_ptr<Activity> targetActivity = nullptr;
    for (const auto& act : user.getActivities()) {
        if (act->getId() == activityId) {
            targetActivity = act;
            break;
        }
    }
    if (!targetActivity) {
        throw std::runtime_error("Activity not found.");
    }
    auto cmd = std::make_unique<RemoveActivityCommand>(*repo, currentUserId, targetActivity);
    cmd->execute();
    undoStack.push_back(std::move(cmd));
    redoStack.clear();
}

void Controller::updateActivityOfCurrentUser(const std::string& id, const std::string& type, int duration, int calories, const std::string& date) {
    User& user = repo->getUserById(currentUserId);
    std::shared_ptr<Activity> oldActivity = nullptr;
    for (const auto& act : user.getActivities()) {
        if (act->getId() == id) {
            oldActivity = std::make_shared<Activity>(act->getId(), act->getType(), act->getDuration(), act->getCaloriesBurned(), act->getDate());
            break;
        }
    }
    if (!oldActivity) {
        throw std::runtime_error("Activity not found.");
    }
    auto newActivity = std::make_shared<Activity>(id, type, duration, calories, date);
    auto cmd = std::make_unique<UpdateActivityCommand>(*repo, currentUserId, id, oldActivity, newActivity);
    cmd->execute();
    undoStack.push_back(std::move(cmd));
    redoStack.clear();
}

bool Controller::undo() {
    if (undoStack.empty()) {
        return false;
    }
    auto cmd = std::move(undoStack.back());
    undoStack.pop_back();
    cmd->undo();
    redoStack.push_back(std::move(cmd));
    return true;
}

bool Controller::redo() {
    if (redoStack.empty()) {
        return false;
    }
    auto cmd = std::move(redoStack.back());
    redoStack.pop_back();
    cmd->execute();
    undoStack.push_back(std::move(cmd));
    return true;
}

std::vector<std::shared_ptr<Activity>> Controller::getCurrentUserActivities() const {
    return repo->getUserById(currentUserId).getActivities();
}

std::vector<std::shared_ptr<Activity>> Controller::getFilteredActivities(const ActivitySpecification& spec) const {
    auto all = getCurrentUserActivities();
    std::vector<std::shared_ptr<Activity>> result;
    for (const auto& act : all) {
        if (spec.isSatisfiedBy(act)) {
            result.push_back(act);
        }
    }
    return result;
}
