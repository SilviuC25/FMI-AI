#ifndef CSVREPOSITORY_H
#define CSVREPOSITORY_H

#include "BaseRepository.h"

class CSVRepository : public BaseRepository {
public:
    CSVRepository(const std::string& filename);

    void loadFromFile() override;
    void saveToFile() override;
};

#endif // CSVREPOSITORY_H
