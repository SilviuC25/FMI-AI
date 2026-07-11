#ifndef BASEREPOSITORY_H
#define BASEREPOSITORY_H

#include "User.h"
#include <vector>
#include <string>

class BaseRepository {
protected:
    std::vector<User> users;
    std::string filename;

public:
    BaseRepository(const std::string& filename) : filename(filename) {}
    virtual ~BaseRepository() = default;

    virtual void loadFromFile() = 0;
    virtual void saveToFile() = 0;

    void addUser(const User& user);
    User& getUserById(const std::string& userId);
    std::vector<User> getAllUsers() const;
};

#endif // BASEREPOSITORY_H
