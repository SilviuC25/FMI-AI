#include "SMMIterator.h"
#include "SortedMultiMap.h"
#include <iostream>
#include <vector>
#include <exception>
using namespace std;

SortedMultiMap::SortedMultiMap(Relation r) {
	// BC = WC = TC = Theta(capacity)
	this->relation = r;
	this->capacity = 10;
	this->mapSize = 0;
	this->root = -1;
	this->firstEmpty = 0;

	this->nodes = new BSTNode[this->capacity];

	for (int i = 0; i < this->capacity - 1; ++i) {
		this->nodes[i].left = i + 1;
		this->nodes[i].right = -1;
	}
	this->nodes[this->capacity - 1].left = -1;
	this->nodes[this->capacity - 1].right = -1;
}

void SortedMultiMap::add(TKey c, TValue v) {
	// BC = Theta(1), WC = Theta(mapSize + capacity), TC = Theta(log2 mapSize)
	if (this->firstEmpty == -1) {
		int oldCapacity = this->capacity;
		this->capacity *= 2;
		BSTNode* newNodes = new BSTNode[this->capacity];

		for (int i = 0; i < oldCapacity; ++i) {
			newNodes[i] = this->nodes[i];
		}

		for (int i = oldCapacity; i < this->capacity - 1; ++i) {
			newNodes[i].left = i + 1;
			newNodes[i].right = -1;
		}
		newNodes[this->capacity - 1].left = -1;
		newNodes[this->capacity - 1].right = -1;

		delete[] this->nodes;
		this->nodes = newNodes;
		firstEmpty = oldCapacity;
	}

	int newNodeIndex = this->firstEmpty;
	this->firstEmpty = this->nodes[this->firstEmpty].left;

	this->nodes[newNodeIndex].info = make_pair(c, v);
	this->nodes[newNodeIndex].left = -1;
	this->nodes[newNodeIndex].right = -1;

	if (this->root == -1) {
		this->root = newNodeIndex;
	} else {
		int currentNode = this->root;
		int parentNode = -1;
		
		while (currentNode != -1) {
			parentNode = currentNode;

			if (this->relation(c, this->nodes[currentNode].info.first)) {
				currentNode = this->nodes[currentNode].left;
			} else {
				currentNode = this->nodes[currentNode].right;
			}
		}

		if (this->relation(c, this->nodes[parentNode].info.first)) {
			this->nodes[parentNode].left = newNodeIndex;
		} else {
			this->nodes[parentNode].right = newNodeIndex;
		}
	}
	this->mapSize++;
}

vector<TValue> SortedMultiMap::search(TKey c) const {
	// BC = Theta(1), WC = Theta(mapSize), TC = Theta(log2 mapSize)
	vector<TValue> values;
	int currentNode = this->root;

	while (currentNode != -1) {
		if (this->nodes[currentNode].info.first == c) {
			values.push_back(this->nodes[currentNode].info.second);
		}

		if (this->relation(c, this->nodes[currentNode].info.first)) {
			currentNode = this->nodes[currentNode].left;
		} else {
			currentNode = this->nodes[currentNode].right;
		}
	}

	return values;
}

bool SortedMultiMap::remove(TKey c, TValue v) {
	// BC = Theta(1), WC = Theta(mapSize), TC = Theta(log2 mapSize)
    int currentNode = this->root;
	int parentNode = -1;

	while (currentNode != -1 && !(this->nodes[currentNode].info.first == c && this->nodes[currentNode].info.second == v)) {
		parentNode = currentNode;
		if (this->relation(c, this->nodes[currentNode].info.first)) {
			currentNode = this->nodes[currentNode].left;
		} else {
			currentNode = this->nodes[currentNode].right;
		}
	}

	if (currentNode == -1) {
		return false;
	}

	if (this->nodes[currentNode].left != -1 && this->nodes[currentNode].right != -1) {
		int minRight = this->nodes[currentNode].right;
		int minRightParent = currentNode;

		while (this->nodes[minRight].left != -1) {
			minRightParent = minRight;
			minRight = this->nodes[minRight].left;
		}

		this->nodes[currentNode].info = this->nodes[minRight].info;
		parentNode = minRightParent;
		currentNode = minRight;
	}

	int child;
	if (this->nodes[currentNode].left != -1) {
		child = this->nodes[currentNode].left;
	} else {
		child = this->nodes[currentNode].right;
	}

	if (currentNode == this->root) {
		this->root = child;
	} else {
		if (parentNode != -1 && this->nodes[parentNode].left == currentNode) {
			this->nodes[parentNode].left = child;
		} else if (parentNode != -1 && this->nodes[parentNode].right == currentNode) {
			this->nodes[parentNode].right = child;
		}
	}

	this->nodes[currentNode].left = this->firstEmpty;
	this->nodes[currentNode].right = -1;
	this->firstEmpty = currentNode;

	this->mapSize--;
	return true;
}


int SortedMultiMap::size() const {
	// BC = WC = TC = Theta(1)
	return this->mapSize;
}

bool SortedMultiMap::isEmpty() const {
	// BC = WC = TC = Theta(1)
	return this->mapSize == 0;
}

SMMIterator SortedMultiMap::iterator() const {
	return SMMIterator(*this);
}

SortedMultiMap::~SortedMultiMap() {
	// BC = WC = TC = Theta(1)
	delete[] this->nodes;
}
