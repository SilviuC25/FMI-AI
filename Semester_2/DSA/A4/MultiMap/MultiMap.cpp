#include "MultiMap.h"
#include "MultiMapIterator.h"
#include <exception>
#include <iostream>

using namespace std;


MultiMap::MultiMap() {
	// BC = WC = TC = Theta(capacity)
	this->capacity = 10;
	this->numElements = 0;
	this->table = new Node*[capacity];
	for (int i = 0; i < capacity; ++i) {
		this->table[i] = nullptr;
	}
}


void MultiMap::add(TKey c, TValue v) {
	// BC = Theta(1), WC = Theta(capacity + numElements), TC = O(1) - amortized
	if ((float) this->numElements / this->capacity > this->loadFactor) {
		int oldCapacity = this->capacity;
		Node** oldTable = table;
		this->capacity = this->capacity * 2;
		table = new Node*[this->capacity];

		for (int i = 0; i < this->capacity; ++i) {
			this->table[i] = nullptr;
		} 

		for (int i = 0; i < oldCapacity; ++i) {
			Node* currentNode = oldTable[i];
			while (currentNode != nullptr) {
				Node* nextNode = currentNode->next;
				int newIndex = this->hash(currentNode->info.first);
				currentNode->next = table[newIndex];
				table[newIndex] = currentNode;
				currentNode = nextNode;
			}
		}
		delete[] oldTable;
	}
	int index = this->hash(c);
	Node* newNode = new Node;
	newNode->info = make_pair(c, v);
	newNode->next = table[index];
	table[index] = newNode;
	this->numElements++;
}


bool MultiMap::remove(TKey c, TValue v) {
	// BC = Theta(1), WC = Theta(numElements), TC = Theta(1)
	int index = this->hash(c);
	Node* currentNode = this->table[index];
	Node *prevNode = nullptr;

	while (currentNode != nullptr) {
		if (currentNode->info.first == c && currentNode->info.second == v) {
			if (prevNode == nullptr) {
				table[index] = currentNode->next;
			} else {
				prevNode->next = currentNode->next;
			}
			delete currentNode;
			this->numElements--;
			return true;
		}
		prevNode = currentNode;
		currentNode = currentNode->next;
	}

	return  false;
}


vector<TValue> MultiMap::search(TKey c) const {
	// BC = Theta(1), WC = Theta(numElements), TC = Theta(1)
	vector<TValue> values;
	int index = this->hash(c);
	Node* currentNode = this->table[index];

	while (currentNode != nullptr) {
		if (currentNode->info.first == c) {
			values.push_back(currentNode->info.second);
		}
		currentNode = currentNode->next;
	}

	return values;
}


int MultiMap::size() const {
	// BC = WC = TC = Theta(1)
	return this->numElements;
}


bool MultiMap::isEmpty() const {
	// BC = WC = TC = Theta(1)
	return this->numElements == 0;
}

MultiMapIterator MultiMap::iterator() const {
	return MultiMapIterator(*this);
}


MultiMap::~MultiMap() {
	// BC = WC = TC = Theta(numElements + capacity)
	for (int i = 0; i < this->capacity; ++i) {
		Node* currentNode = table[i];
		while (currentNode != nullptr) {
			Node* deletedNode = currentNode;
			currentNode = currentNode->next;
			delete deletedNode;
		}
	}

	delete[] table;
}

