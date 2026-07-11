#include "JSONRepository.h"
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <stdexcept>

JSONRepository::JSONRepository(const std::string& filename) : BaseRepository(filename) {
    loadFromFile();
}

void JSONRepository::loadFromFile() {
    QFile file(QString::fromStdString(filename));
    if (!file.open(QIODevice::ReadOnly)) {
        return;
    }

    QByteArray data = file.readAll();
    file.close();

    QJsonDocument doc = QJsonDocument::fromJson(data);
    if (!doc.isArray()) return;

    users.clear();
    QJsonArray usersArray = doc.array();

    for (int i = 0; i < usersArray.size(); ++i) {
        QJsonObject userObj = usersArray[i].toObject();
        std::string uId = userObj["userId"].toString().toStdString();
        std::string uName = userObj["name"].toString().toStdString();

        User user(uId, uName);

        QJsonArray activitiesArray = userObj["activities"].toArray();
        for (int j = 0; j < activitiesArray.size(); ++j) {
            QJsonObject actObj = activitiesArray[j].toObject();

            auto activity = std::make_shared<Activity>(
                actObj["id"].toString().toStdString(),
                actObj["type"].toString().toStdString(),
                actObj["duration"].toInt(),
                actObj["calories"].toInt(),
                actObj["date"].toString().toStdString()
                );
            user.addActivity(activity);
        }
        users.push_back(user);
    }
}

void JSONRepository::saveToFile() {
    QFile file(QString::fromStdString(filename));
    if (!file.open(QIODevice::WriteOnly)) {
        throw std::runtime_error("Could not open JSON file for writing.");
    }

    QJsonArray usersArray;

    for (const auto& user : users) {
        QJsonObject userObj;
        userObj["userId"] = QString::fromStdString(user.getId());
        userObj["name"] = QString::fromStdString(user.getName());

        QJsonArray activitiesArray;
        for (const auto& act : user.getActivities()) {
            QJsonObject actObj;
            actObj["id"] = QString::fromStdString(act->getId());
            actObj["type"] = QString::fromStdString(act->getType());
            actObj["duration"] = act->getDuration();
            actObj["calories"] = act->getCaloriesBurned();
            actObj["date"] = QString::fromStdString(act->getDate());
            activitiesArray.append(actObj);
        }
        userObj["activities"] = activitiesArray;
        usersArray.append(userObj);
    }

    QJsonDocument doc(usersArray);
    file.write(doc.toJson());
    file.close();
}
