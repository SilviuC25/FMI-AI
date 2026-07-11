#include "Movie.h"
#include <string>

using namespace std;

Movie::Movie(string title, string genre, int duration) : title(title), genre(genre), duration(duration) {}

string Movie::getTitle() const {
    return title;
}

string Movie::getGenre() const {
    return genre;
}

int Movie::getDuration() const {
    return duration;
}

