#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QWidget>
#include <QTableWidget>
#include <QListWidget>
#include <QPushButton>
#include <QLineEdit>
#include "SongController.h"

class MainWindow : public QWidget {
    Q_OBJECT

private slots:
    void addSong();
    void deleteSong();
    void updateSong();
    void filterSongs();
    void addToPlaylist();
    void playSong();
    void nextSong();

private:
    SongController *ctrl;

    QTableWidget *tableSongs;
    QListWidget *listPlaylist;
    QLineEdit *editTitle;
    QLineEdit *editArtist;
    QLineEdit *editDuration;
    QLineEdit *editPath;

    void refreshSongsTable();
    void refreshPlaylistWidget();

public:
    MainWindow(SongController *controller, QWidget *parent = nullptr);
    ~MainWindow();
};
#endif
