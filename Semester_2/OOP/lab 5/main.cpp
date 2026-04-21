#include "animal.h"

int main() {
  Animal myAnimal("Tiger", "Panthera tigris");
  Mammal myMammal("Dolphin", "Delphinus delphis", true, 300);
  Bird myBird("Golden Eagle", "Aquila chrysaetos", 220);
  Reptile myReptile("King Cobra", "Ophiophagus hannah", true);

  myAnimal.displayInfo();
  myMammal.displayInfo();
  myBird.displayInfo();
  myReptile.displayInfo();
  
  return 0;
}