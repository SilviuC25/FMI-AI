#include "CSVRepository.h"
#include <fstream>
#include <sstream>

CSVRepository::CSVRepository(const std::string& filename) : BaseRepository(filename) {
    loadFromFile();
}

void CSVRepository::loadFromFile() {
    std::ifstream file(filename);
    if (!file.is_open()) {
        return;
    }

    users.clear();
    std::string line;

    while (std::getline(file, line)) {
        if (line.empty()) continue;

        std::stringstream ss(line);
        std::string uId, uName, aId, aType, durationStr, caloriesStr, date;

        std::getline(ss, uId, ',');
        std::getline(ss, uName, ',');
        std::getline(ss, aId, ',');
        std::getline(ss, aType, ',');
        std::getline(ss, durationStr, ',');
        std::getline(ss, caloriesStr, ',');
        std::getline(ss, date, ',');

        User* currentUser = nullptr;
        for (auto& u : users) {
            if (u.getId() == uId) {
                currentUser = &u;
                break;
            }
        }

        if (!currentUser) {
            users.emplace_back(uId, uName);
            currentUser = &users.back();
        }

        if (!aId.empty()) {
            int duration = std::stoi(durationStr);
            int calories = std::stoi(caloriesStr);
            auto activity = std::make_shared<Activity>(aId, aType, duration, calories, date);
            currentUser->addActivity(activity);
        }
    }
    file.close();
}

void CSVRepository::saveToFile() {
    std::ofstream file(filename);
    if (!file.is_open()) {
        return;
    }

    for (const auto& user : users) {
        auto activities = user.getActivities();
        if (activities.empty()) {
            file << user.getId() << "," << user.getName() << ",,,,, \n";
        } else {
            for (const auto& act : activities) {
                file << user.getId() << ","
                     << user.getName() << ","
                     << act->getId() << ","
                     << act->getType() << ","
                     << act->getDuration() << ","
                     << act->getCaloriesBurned() << ","
                     << act->getDate() << "\n";
            }
        }
    }
    file.close();
}
