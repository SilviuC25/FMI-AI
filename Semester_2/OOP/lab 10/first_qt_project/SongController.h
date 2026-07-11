#ifndef SONGCONTROLLER_H
#define SONGCONTROLLER_H

#include <QVector>
#include "Song.h"

class SongController {
private:
    QVector<Song> allSongs;
    QVector<Song> playlist;

public:
    SongController() {}

    void addSong(const Song& song) {
        allSongs.append(song);
    }

    void removeSong(int index) {
        if (index >= 0 && index < allSongs.size()) {
            Song songToRemove = allSongs[index];
            allSongs.remove(index);

            playlist.removeAll(songToRemove);
        }
    }

    void addToPlaylist(int index) {
        if (index >= 0 && index < allSongs.size()) {
            playlist.append(allSongs[index]);
        }
    }

    const QVector<Song>& getAllSongs() const { return allSongs; }
    const QVector<Song>& getPlaylist() const { return playlist; }
};

#endif
