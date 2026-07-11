#include "Command.h"

AddActivityCommand::AddActivityCommand(BaseRepository& repository, const std::string& uId, std::shared_ptr<Activity> act)
    : repo(repository), userId(uId), activity(act) {}

void AddActivityCommand::execute() {
    repo.getUserById(userId).addActivity(activity);
    repo.saveToFile();
}

void AddActivityCommand::undo() {
    repo.getUserById(userId).removeActivity(activity->getId());
    repo.saveToFile();
}

RemoveActivityCommand::RemoveActivityCommand(BaseRepository& repository, const std::string& uId, std::shared_ptr<Activity> act)
    : repo(repository), userId(uId), activity(act) {}

void RemoveActivityCommand::execute() {
    repo.getUserById(userId).removeActivity(activity->getId());
    repo.saveToFile();
}

void RemoveActivityCommand::undo() {
    repo.getUserById(userId).addActivity(activity);
    repo.saveToFile();
}

UpdateActivityCommand::UpdateActivityCommand(BaseRepository& repository, const std::string& uId, const std::string& actId, std::shared_ptr<Activity> oldAct, std::shared_ptr<Activity> newAct)
    : repo(repository), userId(uId), activityId(actId), oldActivity(oldAct), newActivity(newAct) {}

void UpdateActivityCommand::execute() {
    User& user = repo.getUserById(userId);
    auto activities = user.getActivities();
    for (auto& act : activities) {
        if (act->getId() == activityId) {
            act->setType(newActivity->getType());
            act->setDuration(newActivity->getDuration());
            act->setCaloriesBurned(newActivity->getCaloriesBurned());
            act->setDate(newActivity->getDate());
            break;
        }
    }
    repo.saveToFile();
}

void UpdateActivityCommand::undo() {
    User& user = repo.getUserById(userId);
    auto activities = user.getActivities();
    for (auto& act : activities) {
        if (act->getId() == activityId) {
            act->setType(oldActivity->getType());
            act->setDuration(oldActivity->getDuration());
            act->setCaloriesBurned(oldActivity->getCaloriesBurned());
            act->setDate(oldActivity->getDate());
            break;
        }
    }
    repo.saveToFile();
}
