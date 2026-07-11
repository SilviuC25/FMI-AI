#include <iostream>
#include "Movie.h"
#include "SeriesEpisode.h"
#include "MediaLibrary.h"
#include <string>

using namespace std;

int main() {
    string filename = "library.csv";
    MediaLibrary lib = MediaLibrary(filename);
    lib.displayAll();
    cout << "\n";

    cout << "The Drama Movies are: \n";
    vector<Movie*> dramaMovies = lib.groupByGenre("Drama");
    for (Movie* m : dramaMovies) {
        m->display();
        cout << "\n";
    }

    cout << "\nThe Sci-Fi Movies are: \n";
    vector<Movie*> sciFiMovies = lib.groupByGenre("Sci-Fi");
    for (Movie* m : sciFiMovies) {
        m->display();
        cout << "\n";
    }


    cout << "\n";
    lib.displaySeriesSortedByEpisodes();



    return 0;
}