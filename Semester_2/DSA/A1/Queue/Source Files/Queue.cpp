#include "Queue.h"
#include <exception>
#include <iostream>

using namespace std;


Queue::Queue() {
	// BC = WC = TC = Theta(1)
	this->capacity = 2;
	this->elements = new TElem[this->capacity];
	this->head = 0;
	this->tail = 0;
	this->queueSize = 0;
}



void Queue::push(TElem e) {
	// BC = Theta(1) - when there is enough capacity
	// WC = Theta(queueSize) - when array needs resizing
	// TC = O(queueSize)
	if (this->queueSize == this->capacity) {
		int newCapacity = this->capacity * 2;
		TElem* newElements = new TElem[newCapacity]; 

		for (int i = 0; i < this->queueSize; ++i) {
			newElements[i] = this->elements[(this->head + i) % this->capacity];
		}

		delete[] this->elements;
		this->elements = newElements;
		this->head = 0;
		this->tail = this->queueSize;
		this->capacity = newCapacity;
	}

	this->elements[this->tail] = e;
	this->tail = (this->tail + 1) % this->capacity;
	this->queueSize++;
}


TElem Queue::top() const {
	// BC = WC = TC = Theta(1)
	if (this->isEmpty()) {
		throw exception();
	}

	return this->elements[this->head];
}

TElem Queue::pop() {
	// BC = WC = TC = Theta(1)
	if (this->isEmpty()) {
		throw exception();
	}

	TElem removedElement = this->elements[this->head];
	this->head = (this->head + 1) % this->capacity;
	this->queueSize--;
	return removedElement;
}

bool Queue::isEmpty() const {
	// BC = WC = TC = Theta(1)
	return queueSize == 0;
}


Queue::~Queue() {
	// BC = WC = TC = Theta(1)
	delete[] this->elements;
}

