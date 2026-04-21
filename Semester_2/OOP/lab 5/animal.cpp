#include "animal.h"
#include <iostream>

using namespace std;

Animal::Animal(string commonNameValue, string scientificNameValue) {
  commonName = commonNameValue;
  scientificName = scientificNameValue;
}

void Animal::displayInfo() {
  cout << "Animal:\n" << commonName << " with the scientific name " << scientificName << "\n";
}

// Implementare Mammal
Mammal::Mammal(string commonNameValue, string scientificNameValue, bool isAquaticValue, unsigned int gestationPeriodValue) 
  : Animal(commonNameValue, scientificNameValue) {
  isAquatic = isAquaticValue;
  gestationPeriod = gestationPeriodValue;
}

void Mammal::displayInfo() {
  cout << "Mammal:\n" << commonName << " with the scientific name " << scientificName << "\n";
  if (isAquatic) {
      cout << "It is an aquatic mammal.\n";
  } else {
      cout << "It is not an aquatic mammal.\n";
  }
  cout << "Gestation period: " << gestationPeriod << " days\n";
}

// Implementare Bird
Bird::Bird(string commonNameValue, string scientificNameValue, unsigned int wingSpanValue) 
  : Animal(commonNameValue, scientificNameValue) {
  wingSpan = wingSpanValue;
}

void Bird::displayInfo() {
  cout << "Bird:\n" << commonName << " with the scientific name " << scientificName << "\n";
  cout << "Wingspan: " << wingSpan << " cm\n";
}

// Implementare Reptile
Reptile::Reptile(string commonNameValue, string scientificNameValue, bool isVenomousValue) 
  : Animal(commonNameValue, scientificNameValue) {
  isVenomous = isVenomousValue;
}

void Reptile::displayInfo() {
  cout << "Reptile:\n" << commonName << " with the scientific name " << scientificName << "\n";
  if (isVenomous) {
      cout << "It is a venomous reptile.\n";
  } else {
      cout << "It is not a venomous reptile.\n";
  }
}