#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "BaseRepository.h"
#include "ActivityFilter.h"
#include "Command.h"
#include <memory>
#include <string>
#include <vector>

class Controller {
private:
    std::unique_ptr<BaseRepository> repo;
    std::string currentUserId;
    std::vector<std::unique_ptr<Command>> undoStack;
    std::vector<std::unique_ptr<Command>> redoStack;


public:
    Controller(std::unique_ptr<BaseRepository> repository);

    void setCurrentUser(const std::string& userId);
    std::string getCurrentUserId() const;

    void addUser(const std::string& id, const std::string& name);
    std::vector<User> getAllUsers() const;

    void addActivityToCurrentUser(const std::string& id, const std::string& type, int duration, int calories, const std::string& date);
    void removeActivityFromCurrentUser(const std::string& activityId);
    void updateActivityOfCurrentUser(const std::string& id, const std::string& type, int duration, int calories, const std::string& date);

    bool undo();
    bool redo();

    std::vector<std::shared_ptr<Activity>> getCurrentUserActivities() const;
    std::vector<std::shared_ptr<Activity>> getFilteredActivities(const ActivitySpecification& spec) const;
};

#endif // CONTROLLER_H
