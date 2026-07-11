#pragma once
#ifndef MEDIALIBRARY_H
#define MEDIALIBRARY_H

#include "Movie.h"
#include "SeriesEpisode.h"
#include <vector>


class MediaLibrary {
private:
    std::vector<Movie*> movies;
    void loadFromFile(const std::string& filename);

public:
    MediaLibrary(const std::string& filename);
    std::vector<Movie*> getMovies();
    void add(Movie* newMovie);
    void displayAll();
    std::vector<Movie*> groupByGenre(std::string givenGenre);
    void displaySeriesSortedByEpisodes();
};

#endif