#include "mainwindow.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QLabel>
#include <QHeaderView>
#include <QMessageBox>

MainWindow::MainWindow(SongController *controller, QWidget *parent)
    : QWidget(parent), ctrl(controller) {

    QHBoxLayout *mainLayout = new QHBoxLayout(this);

    QVBoxLayout *leftLayout = new QVBoxLayout();
    leftLayout->addWidget(new QLabel("All songs"));

    tableSongs = new QTableWidget(0, 3);
    tableSongs->setHorizontalHeaderLabels({"Title", "Artist", "Duration"});
    tableSongs->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    tableSongs->setSelectionBehavior(QAbstractItemView::SelectRows);
    leftLayout->addWidget(tableSongs);

    QFormLayout *formLayout = new QFormLayout();
    editTitle = new QLineEdit();
    editArtist = new QLineEdit();
    editDuration = new QLineEdit();
    editPath = new QLineEdit();
    formLayout->addRow("Title:", editTitle);
    formLayout->addRow("Artist:", editArtist);
    formLayout->addRow("Duration:", editDuration);
    formLayout->addRow("Path:", editPath);
    leftLayout->addLayout(formLayout);

    QHBoxLayout *leftButtonsLayout = new QHBoxLayout();
    QPushButton *btnAdd = new QPushButton("Add");
    QPushButton *btnDelete = new QPushButton("Delete");
    QPushButton *btnUpdate = new QPushButton("Update");
    QPushButton *btnFilter = new QPushButton("Filter");
    leftButtonsLayout->addWidget(btnAdd);
    leftButtonsLayout->addWidget(btnDelete);
    leftButtonsLayout->addWidget(btnUpdate);
    leftButtonsLayout->addWidget(btnFilter);
    leftLayout->addLayout(leftButtonsLayout);

    QVBoxLayout *middleLayout = new QVBoxLayout();
    QPushButton *btnMove = new QPushButton(">");
    middleLayout->addStretch();
    middleLayout->addWidget(btnMove);
    middleLayout->addStretch();

    QVBoxLayout *rightLayout = new QVBoxLayout();
    rightLayout->addWidget(new QLabel("Playlist"));
    listPlaylist = new QListWidget();
    rightLayout->addWidget(listPlaylist);
    QPushButton *btnPlay = new QPushButton("Play");
    QPushButton *btnNext = new QPushButton("Next");
    rightLayout->addWidget(btnPlay);
    rightLayout->addWidget(btnNext);

    mainLayout->addLayout(leftLayout);
    mainLayout->addLayout(middleLayout);
    mainLayout->addLayout(rightLayout);

    connect(btnAdd, &QPushButton::clicked, this, &MainWindow::addSong);
    connect(btnDelete, &QPushButton::clicked, this, &MainWindow::deleteSong);
    connect(btnUpdate, &QPushButton::clicked, this, &MainWindow::updateSong);
    connect(btnFilter, &QPushButton::clicked, this, &MainWindow::filterSongs);
    connect(btnMove, &QPushButton::clicked, this, &MainWindow::addToPlaylist);
    connect(btnPlay, &QPushButton::clicked, this, &MainWindow::playSong);
    connect(btnNext, &QPushButton::clicked, this, &MainWindow::nextSong);

    setWindowTitle("Playlist Qt");
    resize(800, 500);
}

MainWindow::~MainWindow() {}

void MainWindow::refreshSongsTable() {
    tableSongs->setRowCount(0);
    for (const Song& s : ctrl->getAllSongs()) {
        int row = tableSongs->rowCount();
        tableSongs->insertRow(row);
        tableSongs->setItem(row, 0, new QTableWidgetItem(s.getTitle()));
        tableSongs->setItem(row, 1, new QTableWidgetItem(s.getArtist()));
        tableSongs->setItem(row, 2, new QTableWidgetItem(QString::number(s.getDuration())));
    }
}

void MainWindow::refreshPlaylistWidget() {
    listPlaylist->clear();
    for (const Song& s : ctrl->getPlaylist()) {
        QString songInfo = s.getTitle() + " - " + s.getArtist();
        listPlaylist->addItem(songInfo);
    }
}

void MainWindow::addSong() {
    QString title = editTitle->text();
    QString artist = editArtist->text();
    int duration = editDuration->text().toInt();
    QString path = editPath->text();

    if (title.isEmpty() || artist.isEmpty()) return;

    Song newSong(title, artist, duration, path);
    ctrl->addSong(newSong);

    refreshSongsTable();

    editTitle->clear();
    editArtist->clear();
    editDuration->clear();
    editPath->clear();
}

void MainWindow::deleteSong() {
    int row = tableSongs->currentRow();
    if (row >= 0) {
        ctrl->removeSong(row);
        refreshSongsTable();
        refreshPlaylistWidget();
    }
}

void MainWindow::updateSong() {
}

void MainWindow::filterSongs() {
    QString filterText = editTitle->text();
    for (int i = 0; i < tableSongs->rowCount(); ++i) {
        bool match = tableSongs->item(i, 0)->text().contains(filterText, Qt::CaseInsensitive);
        tableSongs->setRowHidden(i, !match);
    }
}

void MainWindow::addToPlaylist() {
    int row = tableSongs->currentRow();
    if (row >= 0) {
        ctrl->addToPlaylist(row);
        refreshPlaylistWidget();
    }
}

void MainWindow::playSong() {
    int currentRow = listPlaylist->currentRow();
    if (currentRow >= 0 && currentRow < ctrl->getPlaylist().size()) {
        QString path = ctrl->getPlaylist()[currentRow].getMediaPath();
    }
}

void MainWindow::nextSong() {
    int count = listPlaylist->count();
    if (count == 0) return;

    int currentRow = listPlaylist->currentRow();

    int nextRow = (currentRow + 1) % count;
    listPlaylist->setCurrentRow(nextRow);

    playSong();
}
