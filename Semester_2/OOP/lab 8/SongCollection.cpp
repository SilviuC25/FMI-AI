#include "SongCollection.h"
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <map>
#include <set>
#include <algorithm>

using namespace std;

SongCollection::SongCollection(const string& filePath) {
    loadFromFile(filePath);
}

void SongCollection::loadFromFile(const string& filePath) {
    ifstream file(filePath);
    if (!file.is_open()) {
        throw invalid_argument("Could not open file: " + filePath);
    }

    string line;
    string currentArtist;
    string currentTitle;
    string currentLyrics;
    bool readingLyrics = false;

    while (getline(file, line)) {
        if (line.find("__Artist: ") == 0) {
            if (readingLyrics) {
                songs.push_back(Song(currentArtist, currentTitle, currentLyrics));
                currentLyrics = "";
                readingLyrics = false;
            }
            currentArtist = line.substr(10);
        } else if (line.find("__Song: ") == 0) {
            currentTitle = line.substr(8);
        } else if (line.find("__Lyrics:") == 0) {
            readingLyrics = true;
        } else if (readingLyrics) {
            if (!line.empty()) {
                currentLyrics += line + " ";
            }
        }
    }
    
    if (readingLyrics) {
        songs.push_back(Song(currentArtist, currentTitle, currentLyrics));
    }
    
    file.close();
}

vector<Song> SongCollection::getSongs() const {
    return songs;
}

set<string> SongCollection::getUniqueArtists() const {
    set<string> uniqueArtists;
    
    for (const auto& song : songs) {
        uniqueArtists.insert(song.getArtist());
    }
    
    return uniqueArtists;
}

void SongCollection::printTopArtists() const {
    map<string, vector<Song>> artistBuckets;
    for (const auto& song : songs) {
        artistBuckets[song.getArtist()].push_back(song);
    }

    vector<pair<string, int>> artistCounts;
    for (const auto& entry : artistBuckets) {
        artistCounts.push_back({entry.first, (int)entry.second.size()});
    }

    sort(artistCounts.begin(), artistCounts.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
        return a.second > b.second;
    });

    cout << "Top 10 artists by song count:\n";
    int limit = min((int)artistCounts.size(), 10);
    for (int i = 0; i < limit; ++i) {
        cout << i + 1 << ". " << artistCounts[i].first << " (" << artistCounts[i].second << " songs)\n";
    }
}
