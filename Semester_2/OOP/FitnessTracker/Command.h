#ifndef COMMAND_H
#define COMMAND_H

#include <string>
#include <memory>
#include "BaseRepository.h"
#include "Activity.h"

class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

class AddActivityCommand : public Command {
private:
    BaseRepository& repo;
    std::string userId;
    std::shared_ptr<Activity> activity;

public:
    AddActivityCommand(BaseRepository& repository, const std::string& uId, std::shared_ptr<Activity> act);
    void execute() override;
    void undo() override;
};

class RemoveActivityCommand : public Command {
private:
    BaseRepository& repo;
    std::string userId;
    std::shared_ptr<Activity> activity;

public:
    RemoveActivityCommand(BaseRepository& repository, const std::string& uId, std::shared_ptr<Activity> act);
    void execute() override;
    void undo() override;
};

class UpdateActivityCommand : public Command {
private:
    BaseRepository& repo;
    std::string userId;
    std::string activityId;
    std::shared_ptr<Activity> oldActivity;
    std::shared_ptr<Activity> newActivity;

public:
    UpdateActivityCommand(BaseRepository& repository, const std::string& uId, const std::string& actId, std::shared_ptr<Activity> oldAct, std::shared_ptr<Activity> newAct);
    void execute() override;
    void undo() override;
};

#endif // COMMAND_H
