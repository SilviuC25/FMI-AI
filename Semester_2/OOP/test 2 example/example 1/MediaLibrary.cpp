#include "Movie.h"
#include "SeriesEpisode.h"
#include "MediaLibrary.h"
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <map>
#include <algorithm>

using namespace std;

MediaLibrary::MediaLibrary(const string& filename) {
    this->loadFromFile(filename);
}

void MediaLibrary::add(Movie* newMovie) {
    this->movies.push_back(newMovie);
}

vector<Movie*> MediaLibrary::getMovies() {
    return this->movies;
}

void MediaLibrary::displayAll() {
    for (Movie* m : this->getMovies()) {
        m->display();
        cout << "\n";
    }
}

void MediaLibrary::loadFromFile(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        throw invalid_argument("Could not open " + filename);
    }

    string line;
    
    while (getline(file, line)) {
        if (line.empty()) {
            continue;
        }

        string type, title, genre, seriesName, durationStr, episodeNumberStr;
        stringstream ss(line);

        getline(ss, type, ',');
        getline(ss, title, ',');
        getline(ss, genre, ',');
        getline(ss, durationStr, ',');
        getline(ss, seriesName, ',');
        getline(ss, episodeNumberStr, ',');

        int duration = (durationStr.empty()) ? 0 : stoi(durationStr);
        
        if (type == "Movie") {
            Movie* newMovie = new Movie(title, genre, duration);
            this->add(newMovie);
        } else {
            int episodeNumber = (episodeNumberStr.empty()) ? 0 : stoi(episodeNumberStr);
            SeriesEpisode* newSeriesEpisode = new SeriesEpisode(title, genre, duration, seriesName, episodeNumber);
            this->add(newSeriesEpisode);
        }
    }
}

vector<Movie*> MediaLibrary::groupByGenre(string givenGenre) {
    map<string, vector<Movie*>> movieList;
    for (Movie* m : this->getMovies()) {
        string currentGenre = m->getGenre();
        movieList[currentGenre].push_back(m);
    }

    return movieList[givenGenre];
}

void MediaLibrary::displaySeriesSortedByEpisodes() {
    map<string, vector<Movie*>> seriesList;
    for (Movie* m : this->getMovies()) {
        if (m->getAttributeCount() != 5) {
            continue;
        }
        SeriesEpisode* ep = static_cast<SeriesEpisode*>(m);
        string series = ep->getSeriesName();
        seriesList[series].push_back(m);
    }

    cout << "All Series Lists Sorted By Episode Number:\n";
    for (auto [s, v] : seriesList) {
        sort(v.begin(), v.end(), [] (Movie* a, Movie* b) {
            SeriesEpisode* epA = static_cast<SeriesEpisode*>(a);
            SeriesEpisode* epB = static_cast<SeriesEpisode*>(b);
            int numA = epA->getEpisodeNumber();
            int numB = epB->getEpisodeNumber();

            return numA < numB;
        });

        cout << "\nThe Episodes from Series " << s << " are:\n";

        for (Movie* m : v) {
            m->display();
            cout << "\n";
        }
    }


}