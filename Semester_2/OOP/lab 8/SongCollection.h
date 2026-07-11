#ifndef SONGCOLLECTION_H
#define SONGCOLLECTION_H

#include "Song.h"
#include <vector>
#include <string>
#include <set>
#include <map>
#include <algorithm>

class SongCollection {
private:
    std::vector<Song> songs;
    void loadFromFile(const std::string& filePath);

public:
    SongCollection(const std::string& filePath);
    std::vector<Song> getSongs() const;
    std::set<std::string> getUniqueArtists() const;
    void printTopArtists() const;
};

#endif