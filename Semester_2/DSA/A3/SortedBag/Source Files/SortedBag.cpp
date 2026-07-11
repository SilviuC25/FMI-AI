#include "SortedBag.h"
#include "SortedBagIterator.h"

SortedBag::SortedBag(Relation r) {
	// BC = WC = TC = Theta(capacity)
	this->relation = r;
	this->capacity = 2;
	this->head = -1;
	this->tail = -1;
	this->count = 0;
	this->firstEmpty = 0;
	this->nodes = new Node[this->capacity];

	for (int i = 0; i < this->capacity - 1; ++i) {
		this->nodes[i].next = i + 1;
		this->nodes[i].prev = -1;
	}
	this->nodes[this->capacity - 1].next = -1;
	this->nodes[this->capacity - 1].prev = -1;
}

void SortedBag::add(TComp e) {
	// BC = Theta(1), WC = Theta(capacity + uniqueNodes), TC = Theta(uniqueNodes) - amortized
	int current = this->head;

	while (current != -1) {
		if (this->nodes[current].info == e) {
			this->nodes[current].frequency++;
			this->count++;
			return;
		}
		current = this->nodes[current].next;
	}

	if (this->firstEmpty == -1) {
		int prevCapacity = this->capacity;
		this->capacity *= 2;
		Node* newNodes = new Node[this->capacity];

		for (int i = 0; i < prevCapacity; ++i) {
			newNodes[i] = this->nodes[i];
		}

		for (int i = prevCapacity; i < this->capacity - 1; ++i) {
			newNodes[i].next = i + 1;
			newNodes[i].prev = -1;
		}
		newNodes[this->capacity - 1].next = -1;
		newNodes[this->capacity - 1].prev = -1;

		delete[] this->nodes;
		this->nodes = newNodes;
		this->firstEmpty = prevCapacity;
	}

	int newPos = this->firstEmpty;
	this->firstEmpty = this->nodes[this->firstEmpty].next;

	this->nodes[newPos].info = e;
	this->nodes[newPos].frequency = 1;

	if (this->head == -1) {
		this->head = newPos;
		this->tail = newPos;
		this->nodes[newPos].next = -1;
		this->nodes[newPos].prev = -1;
	} else {
		int findPos = this-> head;

		while (findPos != -1 && this->relation(this->nodes[findPos].info, e)) {
			findPos = this->nodes[findPos].next;
		}

		if (findPos == this->head) {
			this->nodes[newPos].next = this->head;
			this->nodes[newPos].prev = -1;
			this->nodes[this->head].prev = newPos;
			this->head = newPos;
		} else if (findPos == -1) {
			this->nodes[newPos].next = -1;
			this->nodes[newPos].prev = this->tail;
			this->nodes[this->tail].next = newPos;
			this->tail = newPos;
		} else {
			int prevNode = this->nodes[findPos].prev;
			this->nodes[newPos].next = findPos;
			this->nodes[newPos].prev = prevNode;
			this->nodes[findPos].prev = newPos;
			this->nodes[prevNode].next = newPos;
		}
	}

	this->count++;
}


bool SortedBag::remove(TComp e) {
	// BC = Theta(1), WC = Theta(uniqueNodes), TC = Theta(uniqueNodes)
	int current = this->head;

	while (current != -1 && this->nodes[current].info != e) {
		if (!this->relation(this->nodes[current].info, e)) {
			return false;
		}
		current = this->nodes[current].next;
	}

	if (current == -1 || this->nodes[current].info != e) {
		return false;
	}

	if (this->nodes[current].frequency > 1) {
		this->nodes[current].frequency--;
	} else {
		int prevNode = this->nodes[current].prev;
		int nextNode = this->nodes[current].next;

		if (prevNode == -1) {
			this->head = nextNode;
		} else {
			this->nodes[prevNode].next = nextNode;
		}

		if (nextNode == -1) {
			this->tail = prevNode;
		} else {
			this->nodes[nextNode].prev = prevNode;
		}

		this->nodes[current].next = this->firstEmpty;
		this->nodes[current].prev = -1;
		this->firstEmpty = current;
	}

	this->count--;
	return true;
}


bool SortedBag::search(TComp elem) const {
	// BC = Theta(1), WC = Theta(uniqueNodes), TC = Theta(uniqueNodes)
	int current = this->head;

	while (current != -1) {
		if (this->nodes[current].info == elem) {
			return true;
		}

		if (!this->relation(this->nodes[current].info, elem)) {
			break;
		}

		current = this->nodes[current].next;
	}

	return false;
}


int SortedBag::nrOccurrences(TComp elem) const {
	// BC = Theta(1), WC = Theta(uniqueNodes), TC = Theta(uniqueNodes)
	int current = this->head;

	while (current != -1) {
		if (this->nodes[current].info == elem) {
			return this->nodes[current].frequency;
		}

		if (!this->relation(this->nodes[current].info, elem)) {
			break;
		}

		current = this->nodes[current].next;
	}

	return 0;
}



int SortedBag::size() const {
	// BC = WC = TC = Theta(1)
	return this->count;
}


bool SortedBag::isEmpty() const {
	// BC = WC = TC = Theta(1)
	return this->head == -1;
}


SortedBagIterator SortedBag::iterator() const {
	return SortedBagIterator(*this);
}


SortedBag::~SortedBag() {
	// BC = WC = TC = Theta(1)
	delete[] this->nodes;
}
