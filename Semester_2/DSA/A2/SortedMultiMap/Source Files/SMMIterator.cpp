#include "SMMIterator.h"
#include "SortedMultiMap.h"

SMMIterator::SMMIterator(const SortedMultiMap& d) : map(d){
	// BC = WC = TC = Theta(1)
	this->currentNode = d.head;
}

void SMMIterator::first(){
	// BC = WC = TC = Theta(1)
	this->currentNode = map.head;
}

void SMMIterator::next(){
	// BC = WC = TC = Theta(1)
	if (!this->valid()) {
		throw exception();
	}
	this->currentNode = this->currentNode->next;
}

bool SMMIterator::valid() const{
	// BC = WC = TC = Theta(1)
	return this->currentNode != nullptr;
}

TElem SMMIterator::getCurrent() const{
	// BC = WC = TC = Theta(1)
	if (!this->valid()) {
		throw exception();
	}
	return this->currentNode->info;
}


