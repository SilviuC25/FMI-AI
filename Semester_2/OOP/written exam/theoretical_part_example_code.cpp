#include <iostream>
#include <stdexcept>
#include <string>
#include <memory>
#include <vector>
using namespace std;

class Animal {
protected:
    string name;

public:
    Animal(string n) : name(n) {}
    ~Animal() {}

    virtual void speak() {
        cout << name << " says: ..." << "\n";
    }

    void describe() {
        cout << "I am an animal named " << name << "\n";
    }
};

class Dog : public Animal {
    int* tricks;

public:
    Dog(string n, int numTricks) : Animal(n) {
        tricks = new int[numTricks];
    }
    virtual ~Dog() {delete [] tricks;}
    
    void speak() override {
        cout << name << " says: Woof!\n";
    } 
    void describe() {
        cout << "I am a dog named " << name << "\n";
    }
};

class Cat : public Animal {
public:
    Cat(string n) : Animal(n) {}
    void speak() override {
        cout << name << " says: Meow!\n";
    }
};

void makeSpeak(Animal a) {
    a.speak();
}

void makeSpeakRef(Animal& a) {
    a.speak();
}

void riskyFunc0() {
    Dog d("Rex", 5);
    throw runtime_error("Something went wrong");
    std::cout << "Ooops!";
}

void riskyFunk() {
    riskyFunc0();
}

int main() {
    Dog rex("Rex", 3);
    makeSpeak(rex);
    makeSpeakRef(rex);

    vector<unique_ptr<Animal>> zoo;

    zoo.push_back(make_unique<Dog>("Rex", 3));
    zoo.push_back(make_unique<Cat>("Tom"));
    zoo.push_back(make_unique<Cat>("Luna"));
    zoo.push_back(make_unique<Dog>("Rex", 2));

    for (auto& animal : zoo) {
        animal->describe();
        animal->speak();
    }

    try {
        riskyFunk();
    } catch (exception& e) {
        cout << "Caught: " << e.what() << "\n";
    } catch (runtime_error& err) {
        cout << "Caught runtime error: " << err.what() << "\n";
    }

    return 0;
}