#include "BaseRepository.h"
#include <stdexcept>

void BaseRepository::addUser(const User& user) {
    for (const auto& u : users) {
        if (u.getId() == user.getId()) {
            throw std::runtime_error("User with this ID already exists.");
        }
    }
    users.push_back(user);
    saveToFile();
}

User& BaseRepository::getUserById(const std::string& userId) {
    for (auto& u : users) {
        if (u.getId() == userId) {
            return u;
        }
    }
    throw std::runtime_error("User not found.");
}

std::vector<User> BaseRepository::getAllUsers() const {
    return users;
}
