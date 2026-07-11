#include <iostream>
#include <string>
#include <vector>
#include "SortedMultiMap.h"
#include "SMMIterator.h"

using namespace std;

bool relationInt(int a, int b) {
    return a <= b;
}

bool relationString(string a, string b) {
    return a <= b;
}

bool relationChar(char a, char b) {
    return a <= b;
}

int main() {
    try {
        SortedMultiMap<int, int> smmInt(relationInt);
        smmInt.add(10, 100);
        smmInt.add(5, 50);
        smmInt.add(10, 200);
        cout << "SMM<int, int> size: " << smmInt.size() << endl;

        SortedMultiMap<string, int> smmString(relationString);
        smmString.add("Tesla", 2023);
        smmString.add("BMW", 2021);
        smmString.add("Porsche", 2024);
        cout << "SMM<string, int> size: " << smmString.size() << endl;

        SortedMultiMap<char, string> smmChar(relationChar);
        smmChar.add('z', "Last");
        smmChar.add('a', "First");
        smmChar.add('m', "Middle");
        cout << "SMM<char, string> size: " << smmChar.size() << endl;

        cout << "\nIterating through SMM<char, string>:" << endl;
        SMMIterator<char, string> it = smmChar.iterator();
        while (it.valid()) {
            pair<char, string> element = it.getCurrent();
            cout << "Key: " << element.first << " | Value: " << element.second << endl;
            it.next();
        }

        cout << "\nTesting exception handling:" << endl;
        try {
            it.next();
        } catch (const exception& e) {
            cout << "Exception: Iterator is invalid!" << endl;
        }

    } catch (const exception& e) {
        cout << "Unexpected Exception." << endl;
    }

    return 0;
}