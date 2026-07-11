#ifndef SONG_H
#define SONG_H

#include <QString>

class Song {
private:
    QString title;
    QString artist;
    int duration;
    QString mediaPath;

public:
    Song(QString t, QString a, int d, QString path)
        : title(t), artist(a), duration(d), mediaPath(path) {}

    QString getTitle() const { return title; }
    QString getArtist() const { return artist; }
    int getDuration() const { return duration; }
    QString getMediaPath() const { return mediaPath; }

    bool operator==(const Song& other) const {
        return title == other.title && artist == other.artist && duration == other.duration;
    }
};

#endif
