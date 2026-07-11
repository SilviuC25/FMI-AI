#pragma once
#include <exception>
#include <utility>

template <typename TKey, typename TValue>
class SortedMultiMap;

template <typename TKey, typename TValue>
class SMMIterator {
    friend class SortedMultiMap<TKey, TValue>;
private:
    const SortedMultiMap<TKey, TValue>& map;
    SMMIterator(const SortedMultiMap<TKey, TValue>& map) : map(map) {
        this->currentNode = map.head;
    }

    typename SortedMultiMap<TKey, TValue>::Node* currentNode;

public:
    void first() {
        this->currentNode = map.head;
    }

    void next() {
        if (!this->valid()) {
            throw std::exception();
        }
        this->currentNode = this->currentNode->next;
    }

    bool valid() const {
        return this->currentNode != nullptr;
    }

    std::pair<TKey, TValue> getCurrent() const {
        if (!this->valid()) {
            throw std::exception();
        }
        return this->currentNode->info;
    }
};