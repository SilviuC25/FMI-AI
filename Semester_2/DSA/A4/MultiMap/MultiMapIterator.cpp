#include "MultiMapIterator.h"
#include "MultiMap.h"


MultiMapIterator::MultiMapIterator(const MultiMap& c): col(c) {
	// BC = WC = TC = Theta(1);
	this->first();
}

TElem MultiMapIterator::getCurrent() const{
	// BC = WC = TC = Theta(1)
	if (!this->valid()) {
		throw exception();
	}
	return this->currentNode->info;
}

bool MultiMapIterator::valid() const {
	// BC = WC = TC = Theta(1)
	return this->currentNode != nullptr;
}

void MultiMapIterator::next() {
	// BC = Theta(1), WC = Theta(capacity), TC = Theta(1)
	if (!this->valid()) {
		throw exception();
	}
	this->currentNode = this->currentNode->next;

	if (currentNode == nullptr) {
		this->currentIndex++;
		while (this->currentIndex < col.capacity && col.table[this->currentIndex] == nullptr) {
			this->currentIndex++;
		}

		if (this->currentIndex < col.capacity) {
			this->currentNode = col.table[this->currentIndex];
		}
	}
}

void MultiMapIterator::first() {
	// BC = Theta(1), WC = Theta(capacity), TC = Theta(1)
	this->currentIndex = 0;
	while (this->currentIndex < col.capacity && col.table[this->currentIndex] == nullptr) {
		this->currentIndex++;
	}

	if (this->currentIndex < col.capacity) {
		this->currentNode = col.table[currentIndex];
	} else {
		this->currentNode = nullptr;
	}
}

