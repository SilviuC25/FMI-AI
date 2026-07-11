#pragma once

#include <vector>
#include <utility>
#include <exception>

template <typename TKey, typename TValue>
class SMMIterator;

template <typename TKey, typename TValue>
class SortedMultiMap {
    friend class SMMIterator<TKey, TValue>;
private:
    struct Node {
        std::pair<TKey, TValue> info;
        Node* next;
    };

    Node* head;
    bool (*relation)(TKey, TKey);
    int mapSize;

public:
    SortedMultiMap(bool (*r)(TKey, TKey)) {
        this->head = nullptr;
        this->relation = r;
        this->mapSize = 0;
    }

    void add(TKey c, TValue v) {
        Node* newNode = new Node;
        newNode->info = std::make_pair(c, v);
        newNode->next = nullptr;

        if (this->head == nullptr || this->relation(c, this->head->info.first)) {
            newNode->next = this->head;
            this->head = newNode;
        } else {
            Node* currentNode = this->head;
            while (currentNode->next != nullptr && this->relation(currentNode->next->info.first, c)) {
                currentNode = currentNode->next;
            }
            newNode->next = currentNode->next;
            currentNode->next = newNode;
        }
        this->mapSize++;
    }

    std::vector<TValue> search(TKey c) const {
        std::vector<TValue> values;
        Node* currentNode = this->head;

        while (currentNode != nullptr) {
            if (currentNode->info.first == c) {
                values.push_back(currentNode->info.second);
            } else {
                if (!this->relation(currentNode->info.first, c)) {
                    break;
                }
            }
            currentNode = currentNode->next;
        }
        return values;
    }

    bool remove(TKey c, TValue v) {
        Node* currentNode = this->head;
        Node* prevNode = nullptr;

        while (currentNode != nullptr) {
            if (currentNode->info.first == c && currentNode->info.second == v) {
                if (prevNode == nullptr) {
                    this->head = currentNode->next;
                } else {
                    prevNode->next = currentNode->next;
                }
                delete currentNode;
                this->mapSize--;
                return true;
            }
            prevNode = currentNode;
            currentNode = currentNode->next;
        }
        return false;
    }

    int size() const {
        return this->mapSize;
    }

    bool isEmpty() const {
        return this->head == nullptr;
    }

    SMMIterator<TKey, TValue> iterator() const {
        return SMMIterator<TKey, TValue>(*this);
    }

    ~SortedMultiMap() {
        Node* currentNode = this->head;
        while (currentNode != nullptr) {
            Node* nextNode = currentNode->next;
            delete currentNode;
            currentNode = nextNode;
        }
        this->head = nullptr;
    }
};