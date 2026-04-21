#include "Stack.h"
#include <exception>


using namespace std;


Stack::Stack() {
	// BC = WC = TC = Theta(1)
	this->capacity = 2;
	this->elements = new TElem[capacity];
	this->stackSize = 0;
}


void Stack::push(TElem e) {
	// BC = Theta(1) - when there is enough capacity
	// WC = Theta(stackSize) - when array needs resizing
	// TC = O(stackSize)
	if (this->capacity == this->stackSize) {
		this->capacity *= 2;
		TElem* newElements = new TElem[this->capacity];
		for (int i = 0; i < this->stackSize; ++i) {
			newElements[i] = this->elements[i];
		}
		delete[] this->elements;
		this->elements = newElements;
	}
	this->elements[stackSize] = e;
	this->stackSize++;
}

TElem Stack::top() const {
	// BC = WC = TC = Theta(1)
	if (this->isEmpty()) {
		throw exception();
	}
	return this->elements[this->stackSize - 1];
}

TElem Stack::pop() {
	// BC = WC = TC = Theta(1)
	if (this->isEmpty()) {
		throw exception();
	}
	this->stackSize--;
	return this->elements[this->stackSize];
}


bool Stack::isEmpty() const {
	// BC = WC = TC = Theta(1)
	return this->stackSize == 0;
}

Stack::~Stack() {
	// BC = WC = TC = Theta(1)
	delete[] this->elements;
}