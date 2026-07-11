#include "Song.h"
#include <cctype>
#include <string>
#include <vector>

using namespace std;

Song::Song(string artist, string title, string lyrics) 
    : artist(artist), title(title) {
    string currentWord = "";
    
    for (char c : lyrics) {
        if (isalpha(c)) {
            currentWord += tolower(c);
        } else {
            if (!currentWord.empty()) {
                lyricsWords.push_back(currentWord);
                currentWord = "";
            }
        }
    }
    if (!currentWord.empty()) {
        lyricsWords.push_back(currentWord);
    }
}

string Song::getArtist() const {
    return artist;
}

string Song::getTitle() const {
    return title;
}

vector<string> Song::getLyricsWords() const {
    return lyricsWords;
}