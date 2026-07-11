#include "SeriesEpisode.h"
#include "Movie.h"
#include <iostream>
#include <string>

using namespace std;

SeriesEpisode::SeriesEpisode(string titleValue, string genreValue, int durationValue, string seriesNameValue, int episodeNumberValue)
    : Movie(titleValue, genreValue, durationValue) {
        seriesName = seriesNameValue;
        episodeNumber = episodeNumberValue;
}

string SeriesEpisode::getSeriesName() {
    return seriesName;
}

int SeriesEpisode::getEpisodeNumber() {
    return episodeNumber;
}


