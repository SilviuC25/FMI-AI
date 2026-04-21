#include <iostream>

using namespace std;

class DoubleEndedQueue {
  private:
    int* deque_data;
    int deque_length;
    int deque_capacity;

  public:
    DoubleEndedQueue(int capacity = 10):deque_data{new int[capacity]}, deque_length{0}, deque_capacity{capacity}{}

    unsigned int length() const {
      return deque_length;
    }
    unsigned int capacity() const {
      return deque_capacity;
    }

    void push_front(int value) {
      if (deque_capacity >= deque_length) {
        deque_capacity *= 2;
      }
      
      for (unsigned int i = deque_length; i > 0; --i) {
        deque_data[i] = deque_data[i - 1];
      }
      ++deque_length;
      deque_data[0] = value;
    }

    void push_back(int value) {
      if (deque_capacity >= deque_length) {
        deque_capacity *= 2;
      }

      deque_data[deque_length] = value;
      ++deque_length;
    }

    bool pop_front() {
      if (deque_length < 1) {
        return false;
      }
      --deque_length;
      for (unsigned int i = 0; i < deque_length; ++i) {
        deque_data[i] = deque_data[i + 1];
      }
      return true;
    }

    bool pop_back() {
      if (deque_length > 0) {
        --deque_length;
        return true;
      }
      return false;
    }

    int top() {
      return deque_data[0];
    }

    int back() {
      return deque_data[deque_length - 1];
    }

    friend istream& operator>>(istream& is, DoubleEndedQueue& deq) {
      is >> deq.deque_length;
      for (unsigned int i = 0; i < deq.deque_length; ++i) {
        is >> deq.deque_data[i];
      }
      return is;
    }

    friend ostream& operator<<(ostream& os, const DoubleEndedQueue& deq) {
      os << "The length of the queue is: " << deq.deque_length << "\n";
      os << "The elements of the deque are: ";
      for (unsigned int i = 0; i < deq.deque_length; ++i) {
        os << deq.deque_data[i] << " ";
      }
      os << "\n";
      return os;
    }

    ~DoubleEndedQueue(){ 
      if(deque_data){ 
        delete[] deque_data; 
        deque_data = nullptr; 
      } 
    }

    DoubleEndedQueue(const DoubleEndedQueue& other) {
      deque_capacity = other.deque_capacity;
      deque_length = other.deque_length;
      deque_data = new int[deque_capacity]();
      for  (int i = 0; i < deque_length; ++i) {
        deque_data[i] = other.deque_data[i];
      }
    }

    DoubleEndedQueue& operator=(const DoubleEndedQueue& other) {
      if (this != &other) {
        if (deque_data) {
          delete[] deque_data;
        }

        deque_capacity = other.deque_capacity;
        deque_length = other.deque_length;
        deque_data = new int[deque_capacity]();
        for  (int i = 0; i < deque_length; ++i) {
          deque_data[i] = other.deque_data[i];
        }
      }
      return *this;
    }
};

int main() {
  DoubleEndedQueue deq1;
  deq1.push_back(2);
  deq1.push_back(3);
  deq1.push_front(1);

  cout << deq1;

  deq1.push_front(100);
  int num = deq1.top();
  deq1.pop_front();
  deq1.push_back(num);

  cout << deq1;

  DoubleEndedQueue deq2 = deq1;
  
  cout << deq2;
}