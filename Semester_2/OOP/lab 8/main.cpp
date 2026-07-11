#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include "SongCollection.h"

using namespace std;

int main() {
    try {
        SongCollection collection("songs.txt");
        vector<Song> songs = collection.getSongs();

        cout << "--- Unique Artists ---" << endl;
        set<string> artists = collection.getUniqueArtists();
        for (const auto& artist : artists) {
            cout << artist << endl;
        }
        cout << endl;

        cout << "--- Top 10 Artists ---" << endl;
        collection.printTopArtists();
        cout << endl;

        cout << "--- Sort: Artist (Increasing) ---" << endl;
        sort(songs.begin(), songs.end(), [](const Song& a, const Song& b) {
            return a.getArtist() < b.getArtist();
        });
        for(int i=0; i<min((int)songs.size(), 5); ++i) cout << songs[i].getArtist() << " - " << songs[i].getTitle() << endl;
        cout << endl;

        cout << "--- Sort: Title (Descending) ---" << endl;
        sort(songs.begin(), songs.end(), [](const Song& a, const Song& b) {
            return a.getTitle() > b.getTitle();
        });
        for(int i=0; i<min((int)songs.size(), 5); ++i) cout << songs[i].getTitle() << endl;
        cout << endl;

        cout << "--- Sort: Lyrics Word Count (Increasing) ---" << endl;
        sort(songs.begin(), songs.end(), [](const Song& a, const Song& b) {
            return a.getLyricsWords().size() < b.getLyricsWords().size();
        });
        for(int i=0; i<min((int)songs.size(), 5); ++i) cout << songs[i].getLyricsWords().size() << " words: " << songs[i].getTitle() << endl;
        cout << endl;

        map<string, vector<int>> wordIndex;
        for (int i = 0; i < songs.size(); ++i) {
            for (const string& word : songs[i].getLyricsWords()) {
                wordIndex[word].push_back(i);
            }
        }

        string searchWord = "reality";
        cout << "--- Searching for word: " << searchWord << " ---" << endl;
        if (wordIndex.count(searchWord)) {
            for (int index : wordIndex[searchWord]) {
                cout << "Found in: " << songs[index].getTitle() << " by " << songs[index].getArtist() << endl;
            }
        } else {
            cout << "Word not found." << endl;
        }

    } catch (const invalid_argument& e) {
        cout << "Error: " << e.what() << endl;
    }

    return 0;
}