#pragma once
#ifndef SERIESEPISODE_H
#define SERIESEPISODE_H

#include "Movie.h"
#include <string>

class SeriesEpisode : public Movie {
private:
    std::string seriesName;
    int episodeNumber;

public:
    SeriesEpisode(std::string titleValue, std::string genreValue, int durationValue, std::string seriesNameValue, int episodeNumberValue);
    std::string getSeriesName();
    int getEpisodeNumber();

    virtual void display() const override {
        Movie::display();
        std::cout << " | Series Name: " << seriesName << " | Episode Number: " << episodeNumber;
    }

    int getAttributeCount() const override { return 5; }
};

#endif