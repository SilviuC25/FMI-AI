#ifndef SONG_H
#define SONG_H

#include <string>
#include <vector>

class Song {
protected:
    std::string artist;
    std::string title;

private:
    std::vector<std::string> lyricsWords;

public:
    Song(std::string artist, std::string title, std::string lyrics);
    
    std::string getArtist() const;
    std::string getTitle() const;
    std::vector<std::string> getLyricsWords() const;
};

#endif