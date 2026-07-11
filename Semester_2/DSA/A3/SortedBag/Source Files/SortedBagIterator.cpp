#include "SortedBagIterator.h"
#include "SortedBag.h"
#include <exception>

using namespace std;

SortedBagIterator::SortedBagIterator(const SortedBag& b) : bag(b) {
	// BC = WC = TC = Theta(1)
	this->currentPos = b.head;
	this->currentFrequency = 1;
}

TComp SortedBagIterator::getCurrent() {
	// BC = WC = TC = Theta(1)
	if (!this->valid()) {
		throw exception();
	}

	return bag.nodes[this->currentPos].info;
}

bool SortedBagIterator::valid() {
	// BC = WC = TC = Theta(1)
	return this->currentPos != -1;
}

void SortedBagIterator::next() {
	// BC = WC = TC = Theta(1)
	if (!this->valid()) {
		throw exception();
	}

	if (this->currentFrequency < bag.nodes[this->currentPos].frequency) {
		this->currentFrequency++;
	} else {
		this->currentPos = bag.nodes[this->currentPos].next;
		this->currentFrequency = 1;
	}
}

void SortedBagIterator::first() {
	// BC = WC = TC = Theta(1)
	this->currentPos = bag.head;
	this->currentFrequency = 1;
}

