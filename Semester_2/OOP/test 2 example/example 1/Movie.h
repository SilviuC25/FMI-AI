#pragma once
#ifndef MOVIE_H
#define MOVIE_H

#include <string>
#include <iostream>

class Movie {
protected:
    std::string title;
    std::string genre;
    int duration;

public:
    Movie(std::string title, std::string genre, int duration);

    std::string getTitle() const;
    std::string getGenre() const;
    int getDuration() const;


    virtual void display() const {
        std::cout << "Movie: " << title << " | Genre: " << genre << " | Duration: " << duration << " min";
    }

    virtual int getAttributeCount() const { return 3; }
};

#endif