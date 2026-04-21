#include "SMMIterator.h"
#include "SortedMultiMap.h"
#include <iostream>
#include <vector>
#include <exception>
using namespace std;

SortedMultiMap::SortedMultiMap(Relation r) {
	// BC = WC = TC = Theta(1)
	this->head = nullptr;
	this->relation = r;
	this->mapSize = 0;
}

void SortedMultiMap::add(TKey c, TValue v) {
	// BC = Theta(1), WC = TC = Theta(mapSize)
	Node* newNode = new Node;
	newNode->info = make_pair(c, v);
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

vector<TValue> SortedMultiMap::search(TKey c) const {
	// BC = Theta(1), WC = TC = Theta(mapSize)
	vector<TValue> values;
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

bool SortedMultiMap::remove(TKey c, TValue v) {
	// BC = Theta(1), WC = TC = Theta(mapSize)
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


int SortedMultiMap::size() const {
	// BC = WC = TC = Theta(1)
	return mapSize;
}

bool SortedMultiMap::isEmpty() const {
	// BC = WC = TC = Theta(1)
	return this->head == nullptr;
}

SMMIterator SortedMultiMap::iterator() const {
	return SMMIterator(*this);
}

SortedMultiMap::~SortedMultiMap() {
	// BC = WC = TC = Theta(mapSize)
	Node* currentNode = this->head;
	while (currentNode != nullptr) {
		Node* nextNode = currentNode->next;
		delete currentNode;
		currentNode = nextNode;
	}
	this->head = nullptr;
}
