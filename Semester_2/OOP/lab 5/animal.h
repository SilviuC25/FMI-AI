#pragma once

#include <string>

class Animal {
protected:
  std::string commonName;
  std::string scientificName;

public:
  Animal(std::string commonNameValue, std::string scientificNameValue);
  void displayInfo();
};

class Mammal : public Animal {
private:
  bool isAquatic;
  unsigned int gestationPeriod;

public:
  Mammal(std::string commonNameValue, std::string scientificNameValue, bool isAquaticValue, unsigned int gestationPeriodValue);
  void displayInfo();
};

class Bird : public Animal {
private: 
  unsigned int wingSpan;

public:
  Bird(std::string commonNameValue, std::string scientificNameValue, unsigned int wingSpanValue);
  void displayInfo();
};

class Reptile : public Animal {
private: 
  bool isVenomous;

public:
  Reptile(std::string commonNameValue, std::string scientificNameValue, bool isVenomousValue);
  void displayInfo();
};
