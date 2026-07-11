#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include "Volume.h"
#include "Series.h"
#include "LibraryItem.h"
#include "Bookstore.h"

using namespace std;

int main() {
    Bookstore bookstore;
    Volume book1("The Name of the Wind", 32, 4.01, 2002);
    Volume book2("Alice in Wonderland", 10, 4.44, 1999);
    Volume harry1("Harry Potter and the Order of Phoenix", 10, 4.66, 2007);
    Volume harry2("Harry Potter and the Prisoner of Azkaban", 17, 4.33, 2003);
    Volume harry3("Harry Potter and the Philosopher's Stone", 12, 4.8, 2002);
    Volume book3("American Gods", 20, 4.48, 2000);
    Volume book4("Way of Kings", 42, 4.89, 2010);
    Volume book5("The lion, the witch and the wardrobe", 11, 4.22, 1950);
    Volume harry4("Harry Potter and the Half-Blood Price", 13, 4.22, 2005);
    
    Series harryPotter("Harry Potter", 0, 0);
    harryPotter.addVolume(harry1);
    harryPotter.addVolume(harry2);
    harryPotter.addVolume(harry3);
    
    bookstore.addItem(harryPotter);
    bookstore.addItem(book1);
    bookstore.addItem(book2);
    bookstore.addItem(book3);
    bookstore.addItem(book4);
    bookstore.addItem(book5);
    
    try {
        harryPotter.addVolume(harry4);
    } catch (length_error& err) {
        cout << "The following error occured while adding a Volume: " << err.what();
    }
    
    
    
    return 0;
}