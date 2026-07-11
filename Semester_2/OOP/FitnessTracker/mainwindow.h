#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QListWidget>
#include <QPushButton>
#include <QLineEdit>
#include <QLabel>
#include <QComboBox>
#include <QRadioButton>
#include <QButtonGroup>
#include <memory>
#include "Controller.h"

class MainWindow : public QWidget {
    Q_OBJECT

private:
    QVBoxLayout* mainLayout;
    QListWidget* activityListWidget;

    QComboBox* userComboBox;
    QLineEdit* newUserIdLineEdit;
    QLineEdit* newUserNameLineEdit;
    QPushButton* addUserBtn;

    QLineEdit* idLineEdit;
    QLineEdit* typeLineEdit;
    QLineEdit* durationLineEdit;
    QLineEdit* caloriesLineEdit;
    QLineEdit* dateLineEdit;

    QPushButton* addBtn;
    QPushButton* deleteBtn;
    QPushButton* updateBtn;
    QPushButton* undoBtn;
    QPushButton* redoBtn;

    QRadioButton* jsonRadio;
    QRadioButton* csvRadio;
    QButtonGroup* repoGroup;

    QLineEdit* filterTypeLineEdit;
    QLineEdit* filterDurationLineEdit;
    QRadioButton* andRadio;
    QRadioButton* orRadio;
    QPushButton* filterBtn;
    QPushButton* resetFilterBtn;
    bool isFiltered = false;
    std::vector<std::shared_ptr<Activity>> filteredList;

    std::unique_ptr<Controller> controller;


    void setupUI();
    void initConnect();
    void refreshUserComboBox();
    void refreshList();

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow() = default;

private slots:
    void handleAddUser();
    void handleUserChanged(int index);
    void handleAddActivity();
    void handleDeleteActivity();
    void handleUpdateActivity();
    void handleUndo();
    void handleRedo();
    void handleRepoTypeChanged();
    void handleFilter();
    void handleResetFilter();
};

#endif // MAINWINDOW_H
