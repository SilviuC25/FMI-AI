#include "mainwindow.h"
#include "JSONRepository.h"
#include "CSVRepository.h"
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent) {

    auto repo = std::make_unique<JSONRepository>("fitness_data.json");
    controller = std::make_unique<Controller>(std::move(repo));

    setupUI();
    initConnect();
    refreshUserComboBox();
    refreshList();
}

void MainWindow::setupUI() {
    this->resize(700, 650);
    this->setWindowTitle("Fitness Tracker");

    this->setStyleSheet(R"(
        QWidget {
            background-color: #f5f6fa;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #2f3640;
        }
        QLabel {
            font-weight: bold;
            color: #353b48;
        }
        QLineEdit, QComboBox, QListWidget {
            background-color: #ffffff;
            border: 1px solid #dcdde1;
            border-radius: 4px;
            padding: 6px;
            color: #2f3640;
        }
        QLineEdit:focus, QComboBox:focus, QListWidget:focus {
            border: 1px solid #00a8ff;
        }
        QPushButton {
            background-color: #00a8ff;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0097e6;
        }
        QPushButton:pressed {
            background-color: #0086cc;
        }
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #dcdde1;
        }
        QListWidget::item:selected {
            background-color: #00a8ff;
            color: white;
            border-radius: 3px;
        }
        QRadioButton {
            font-weight: bold;
            color: #2f3640;
        }
    )");

    mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(15);
    mainLayout->setContentsMargins(20, 20, 20, 20);

    QHBoxLayout* repoLayout = new QHBoxLayout();
    repoLayout->addWidget(new QLabel("Storage Type:", this));
    jsonRadio = new QRadioButton("JSON Storage", this);
    csvRadio = new QRadioButton("CSV Storage", this);
    jsonRadio->setChecked(true);

    repoGroup = new QButtonGroup(this);
    repoGroup->addButton(jsonRadio);
    repoGroup->addButton(csvRadio);

    repoLayout->addWidget(jsonRadio);
    repoLayout->addWidget(csvRadio);
    repoLayout->addStretch();
    mainLayout->addLayout(repoLayout);

    QHBoxLayout* userLayout = new QHBoxLayout();
    userLayout->addWidget(new QLabel("Select User:", this));
    userComboBox = new QComboBox(this);
    userComboBox->setMinimumWidth(150);
    userLayout->addWidget(userComboBox);

    newUserIdLineEdit = new QLineEdit(this);
    newUserIdLineEdit->setPlaceholderText("New User ID");
    newUserNameLineEdit = new QLineEdit(this);
    newUserNameLineEdit->setPlaceholderText("New User Name");

    addUserBtn = new QPushButton("Add User", this);
    addUserBtn->setStyleSheet("QPushButton { background-color: #4cd137; } QPushButton:hover { background-color: #44bd32; }");

    userLayout->addWidget(newUserIdLineEdit);
    userLayout->addWidget(newUserNameLineEdit);
    userLayout->addWidget(addUserBtn);
    mainLayout->addLayout(userLayout);

    activityListWidget = new QListWidget(this);
    mainLayout->addWidget(activityListWidget);

    QHBoxLayout* filterLayout = new QHBoxLayout();
    filterTypeLineEdit = new QLineEdit(this);
    filterTypeLineEdit->setPlaceholderText("Filter Type");
    filterDurationLineEdit = new QLineEdit(this);
    filterDurationLineEdit->setPlaceholderText("Min Duration");

    andRadio = new QRadioButton("AND", this);
    orRadio = new QRadioButton("OR", this);
    andRadio->setChecked(true);

    filterBtn = new QPushButton("Apply Filter", this);
    resetFilterBtn = new QPushButton("Reset", this);
    resetFilterBtn->setStyleSheet("QPushButton { background-color: #7f8fa6; } QPushButton:hover { background-color: #718093; }");

    filterLayout->addWidget(filterTypeLineEdit);
    filterLayout->addWidget(filterDurationLineEdit);
    filterLayout->addWidget(andRadio);
    filterLayout->addWidget(orRadio);
    filterLayout->addWidget(filterBtn);
    filterLayout->addWidget(resetFilterBtn);
    mainLayout->addLayout(filterLayout);

    QGridLayout* formLayout = new QGridLayout();
    formLayout->setVerticalSpacing(10);

    formLayout->addWidget(new QLabel("Activity ID:", this), 0, 0);
    idLineEdit = new QLineEdit(this);
    formLayout->addWidget(idLineEdit, 0, 1);

    formLayout->addWidget(new QLabel("Type (e.g., Running):", this), 1, 0);
    typeLineEdit = new QLineEdit(this);
    formLayout->addWidget(typeLineEdit, 1, 1);

    formLayout->addWidget(new QLabel("Duration (min):", this), 2, 0);
    durationLineEdit = new QLineEdit(this);
    formLayout->addWidget(durationLineEdit, 2, 1);

    formLayout->addWidget(new QLabel("Calories Burned:", this), 3, 0);
    caloriesLineEdit = new QLineEdit(this);
    formLayout->addWidget(caloriesLineEdit, 3, 1);

    formLayout->addWidget(new QLabel("Date (YYYY-MM-DD):", this), 4, 0);
    dateLineEdit = new QLineEdit(this);
    formLayout->addWidget(dateLineEdit, 4, 1);

    mainLayout->addLayout(formLayout);

    QHBoxLayout* btnLayout = new QHBoxLayout();
    addBtn = new QPushButton("Add Activity", this);
    updateBtn = new QPushButton("Update Activity", this);
    deleteBtn = new QPushButton("Delete Activity", this);
    undoBtn = new QPushButton("Undo", this);
    redoBtn = new QPushButton("Redo", this);

    addBtn->setStyleSheet("QPushButton { background-color: #4cd137; } QPushButton:hover { background-color: #44bd32; }");
    updateBtn->setStyleSheet("QPushButton { background-color: #fbc531; color: #2f3640; } QPushButton:hover { background-color: #e1b12c; }");
    deleteBtn->setStyleSheet("QPushButton { background-color: #e84118; } QPushButton:hover { background-color: #c23616; }");
    undoBtn->setStyleSheet("QPushButton { background-color: #9c88ff; } QPushButton:hover { background-color: #8c7ae6; }");
    redoBtn->setStyleSheet("QPushButton { background-color: #9c88ff; } QPushButton:hover { background-color: #8c7ae6; }");

    btnLayout->addWidget(addBtn);
    btnLayout->addWidget(updateBtn);
    btnLayout->addWidget(deleteBtn);
    btnLayout->addWidget(undoBtn);
    btnLayout->addWidget(redoBtn);

    mainLayout->addLayout(btnLayout);

    this->setLayout(mainLayout);
}

void MainWindow::initConnect() {
    connect(jsonRadio, &QRadioButton::toggled, this, &MainWindow::handleRepoTypeChanged);
    connect(csvRadio, &QRadioButton::toggled, this, &MainWindow::handleRepoTypeChanged);
    connect(addUserBtn, &QPushButton::clicked, this, &MainWindow::handleAddUser);
    connect(userComboBox, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &MainWindow::handleUserChanged);
    connect(addBtn, &QPushButton::clicked, this, &MainWindow::handleAddActivity);
    connect(deleteBtn, &QPushButton::clicked, this, &MainWindow::handleDeleteActivity);
    connect(updateBtn, &QPushButton::clicked, this, &MainWindow::handleUpdateActivity);
    connect(undoBtn, &QPushButton::clicked, this, &MainWindow::handleUndo);
    connect(redoBtn, &QPushButton::clicked, this, &MainWindow::handleRedo);
    connect(filterBtn, &QPushButton::clicked, this, &MainWindow::handleFilter);
    connect(resetFilterBtn, &QPushButton::clicked, this, &MainWindow::handleResetFilter);
}

void MainWindow::handleRepoTypeChanged() {
    if (!jsonRadio->signalsBlocked() && !csvRadio->signalsBlocked()) {
        std::unique_ptr<BaseRepository> newRepo;
        if (jsonRadio->isChecked()) {
            newRepo = std::make_unique<JSONRepository>("fitness_data.json");
        } else {
            newRepo = std::make_unique<CSVRepository>("fitness_data.csv");
        }
        controller = std::make_unique<Controller>(std::move(newRepo));
        refreshUserComboBox();
        refreshList();
    }
}

void MainWindow::refreshUserComboBox() {
    userComboBox->blockSignals(true);
    userComboBox->clear();
    auto users = controller->getAllUsers();
    for (const auto& u : users) {
        userComboBox->addItem(QString::fromStdString(u.getName()), QString::fromStdString(u.getId()));
    }
    int index = userComboBox->findData(QString::fromStdString(controller->getCurrentUserId()));
    if (index != -1) {
        userComboBox->setCurrentIndex(index);
    }
    userComboBox->blockSignals(false);
}

void MainWindow::refreshList() {
    activityListWidget->clear();
    auto activities = isFiltered ? filteredList : controller->getCurrentUserActivities();
    for (const auto& act : activities) {
        QString itemText = QString("ID: %1 | Type: %2 | Duration: %3 min | Calories: %4 kcal | Date: %5")
        .arg(QString::fromStdString(act->getId()))
            .arg(QString::fromStdString(act->getType()))
            .arg(act->getDuration())
            .arg(act->getCaloriesBurned())
            .arg(QString::fromStdString(act->getDate()));
        activityListWidget->addItem(itemText);
    }
}

void MainWindow::handleAddUser() {
    std::string id = newUserIdLineEdit->text().toStdString();
    std::string name = newUserNameLineEdit->text().toStdString();
    if (id.empty() || name.empty()) {
        QMessageBox::warning(this, "Validation Error", "User ID and Name cannot be empty.");
        return;
    }
    try {
        controller->addUser(id, name);
        controller->setCurrentUser(id);
        refreshUserComboBox();
        refreshList();
        newUserIdLineEdit->clear();
        newUserNameLineEdit->clear();
    } catch (const std::exception& e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void MainWindow::handleUserChanged(int index) {
    if (index == -1) return;
    std::string userId = userComboBox->itemData(index).toString().toStdString();
    controller->setCurrentUser(userId);
    refreshList();
}

void MainWindow::handleAddActivity() {
    std::string id = idLineEdit->text().toStdString();
    std::string type = typeLineEdit->text().toStdString();
    int duration = durationLineEdit->text().toInt();
    int calories = caloriesLineEdit->text().toInt();
    std::string date = dateLineEdit->text().toStdString();

    if (id.empty() || type.empty()) {
        QMessageBox::warning(this, "Validation Error", "ID and Type cannot be empty!");
        return;
    }
    try {
        controller->addActivityToCurrentUser(id, type, duration, calories, date);
        refreshList();
        idLineEdit->clear();
        typeLineEdit->clear();
        durationLineEdit->clear();
        caloriesLineEdit->clear();
        dateLineEdit->clear();
    } catch (const std::exception& e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void MainWindow::handleDeleteActivity() {
    std::string id = idLineEdit->text().toStdString();
    if (id.empty()) {
        QMessageBox::warning(this, "Validation Error", "Please provide the Activity ID to delete.");
        return;
    }
    try {
        controller->removeActivityFromCurrentUser(id);
        refreshList();
        idLineEdit->clear();
    } catch (const std::exception& e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void MainWindow::handleUpdateActivity() {
    std::string id = idLineEdit->text().toStdString();
    std::string type = typeLineEdit->text().toStdString();
    int duration = durationLineEdit->text().toInt();
    int calories = caloriesLineEdit->text().toInt();
    std::string date = dateLineEdit->text().toStdString();

    if (id.empty()) {
        QMessageBox::warning(this, "Validation Error", "Please provide the Activity ID to update.");
        return;
    }
    try {
        controller->updateActivityOfCurrentUser(id, type, duration, calories, date);
        refreshList();
    } catch (const std::exception& e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void MainWindow::handleUndo() {
    if (!controller->undo()) {
        QMessageBox::information(this, "Undo", "No more actions to undo.");
    } else {
        refreshList();
    }
}

void MainWindow::handleRedo() {
    if (!controller->redo()) {
        QMessageBox::information(this, "Redo", "No more actions to redo.");
    } else {
        refreshList();
    }
}

void MainWindow::handleFilter() {
    std::string type = filterTypeLineEdit->text().toStdString();
    std::string durStr = filterDurationLineEdit->text().toStdString();

    if (type.empty() && durStr.empty()) {
        isFiltered = false;
        refreshList();
        return;
    }

    std::shared_ptr<ActivitySpecification> typeSpec = std::make_shared<TypeSpecification>(type);
    int minDur = durStr.empty() ? 0 : std::stoi(durStr);
    std::shared_ptr<ActivitySpecification> durSpec = std::make_shared<DurationSpecification>(minDur);

    if (!type.empty() && !durStr.empty()) {
        if (andRadio->isChecked()) {
            AndSpecification andSpec(typeSpec, durSpec);
            filteredList = controller->getFilteredActivities(andSpec);
        } else {
            OrSpecification orSpec(typeSpec, durSpec);
            filteredList = controller->getFilteredActivities(orSpec);
        }
    } else if (!type.empty()) {
        filteredList = controller->getFilteredActivities(*typeSpec);
    } else {
        filteredList = controller->getFilteredActivities(*durSpec);
    }

    isFiltered = true;
    refreshList();
}

void MainWindow::handleResetFilter() {
    filterTypeLineEdit->clear();
    filterDurationLineEdit->clear();
    isFiltered = false;
    refreshList();
}
