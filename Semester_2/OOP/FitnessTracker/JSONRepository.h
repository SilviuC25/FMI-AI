#ifndef JSONREPOSITORY_H
#define JSONREPOSITORY_H

#include "BaseRepository.h"

class JSONRepository : public BaseRepository {
public:
    JSONRepository(const std::string& filename);

    void loadFromFile() override;
    void saveToFile() override;
};

#endif // JSONREPOSITORY_H
