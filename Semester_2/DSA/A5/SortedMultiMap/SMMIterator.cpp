#include "SMMIterator.h"
#include "SortedMultiMap.h"

SMMIterator::SMMIterator(const SortedMultiMap& d) : map(d){
	this->first();
}

void SMMIterator::first(){
	// BC = Theta(1), WC = Theta(mapSize), TC = Theta(log2 mapSize)
	this->currentNode = map.root;

	while (this->currentNode != -1 && this->map.nodes[this->currentNode].left != -1) {
        this->currentNode = this->map.nodes[this->currentNode].left;
    }
}

void SMMIterator::next(){
	// BC = Theta(1), WC = Theta(mapSize), TC = Theta(log2 mapSize)
	if (!this->valid()) {
        throw exception();
    }

    if (this->map.nodes[this->currentNode].right != -1) {
        this->currentNode = this->map.nodes[this->currentNode].right;
        while (this->map.nodes[this->currentNode].left != -1) {
            this->currentNode = this->map.nodes[this->currentNode].left;
        }
    } else {
        int searchNode = this->map.root;
        int nextNode = -1;
        TKey currentKey = this->map.nodes[this->currentNode].info.first;

        while (searchNode != this->currentNode && searchNode != -1) {
            if (this->map.relation(currentKey, this->map.nodes[searchNode].info.first)) {
                nextNode = searchNode;
                searchNode = this->map.nodes[searchNode].left;
            } else {
                searchNode = this->map.nodes[searchNode].right;
            }
        }
        this->currentNode = nextNode;
    }
}

bool SMMIterator::valid() const{
	// BC = WC = TC = Theta(1)
	return this->currentNode != -1;
}

TElem SMMIterator::getCurrent() const{
	// BC = WC = TC = Theta(1)
	if (!this->valid()) {
		throw exception();
	}
	return map.nodes[this->currentNode].info;
}


