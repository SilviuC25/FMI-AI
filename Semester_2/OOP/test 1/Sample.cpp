#include <iostream>
#include <math.h>
#include <stdlib.h>
#include <random>
using namespace std;

class Sample {
private:
    double x;
    double y;
    int label;
    
public:
    Sample(): x(0.0), y(0.0), label(0) {}
    Sample(double xVal, double yVal, int labelVal): x(xVal), y(yVal), label(labelVal) {}

    double getX() {
        return x;
    }
    
    double getY() {
        return y;
    }
    
    int getLabel() {
        return label;
    }
    
    void setX(double xVal) {
        x = xVal;
    }
    
    void setY(double yVal) {
        y = yVal;
    }
    
    void setLabel(int labelVal) {
        label = labelVal;
    }

    friend istream& operator>>(istream& is, Sample& sample) {
        cout << "Enter x: ";
        is >> sample.x;
        cout << "\nEnter y: ";
        is >> sample.y;
        cout << "\nEnter label: ";
        is >> sample.label;
        return is;
    }
    
    friend ostream& operator<<(ostream& os, const Sample& sample) {
        cout << "X is equal to: " << sample.x;
        cout << "\nY is equal to: " << sample.y;
        cout << "\nLabel is equal to: " << sample.label;
        cout << "\n";
        return os;
    }
    
    static double distance(Sample sample1, Sample sample2) {
        double x1 = sample1.getX(), y1 = sample1.getY();
        double x2 = sample2.getX(), y2 = sample2.getY();
        double t1 = x2 - x1, t2 = y2 - y1;
        double dist = sqrt(t1 * t1 + t2 * t2);
        return dist;
    }
    
    friend Sample operator-(Sample sample1, Sample sample2) {
        Sample diffSample;
        double newX = sample1.getX() - sample2.getX(), newY = sample1.getY() - sample2.getY();
        diffSample.setX(newX);
        diffSample.setY(newY);
        return diffSample;
    }
    
    bool operator==(Sample& other) {
        return (other.getX() == this->x) && (other.getY() == this->y) && (other.getLabel() == this->label);
    }
};

class Classifier {
private:
    Sample samples[1000];
    static int bestK;

public:

    int classify(const Sample& query, int k) {
        for (int i = 0; i < 1000 - 1; ++i) {
            for (int j = i + 1; j < 1000; ++j) {
                double distFromI = Sample::distance(samples[i], query);
                double distFromJ = Sample:: distance(samples[j], query);
                if (distFromI > distFromJ) {
                    double tempX = samples[i].getX(), tempY = samples[i].getY(), tempLabel = samples[i].getLabel();
                    samples[i].setX(samples[j].getX());
                    samples[i].setY(samples[j].getY());
                    samples[i].setLabel(samples[j].getLabel());
                    samples[j].setX(tempX);
                    samples[j].setY(tempY);
                    samples[j].setLabel(tempLabel);
                }
            }
        } 
        int count0 = 0, count1 = 0;
        for (int i = 0; i < k; ++i) {
            if (samples[i].getLabel() == 0) {
                ++count0;
            } else {
                ++count1;
            }
        }
        if (count0 >= count1) {
            return 0;
        }
        return 1;
    }
    
    double accuracy(Sample sampleSet[], int sampleSetSize, int k) {
        double accuracyValue = 0.0;
        int count;
        for (int i = 0; i < sampleSetSize; ++i) {
            int predict = classify(sampleSet[i], k);
            if (predict == sampleSet[i].getLabel()) {
                ++count;
            }
        }
        accuracyValue = (double) count / sampleSetSize;
        return accuracyValue;
    }
    
    int findBestK(const Sample set[], int setSize(), int maxK) {
        return 0;
    }
};

Sample samples[1000];
static int bestK;

double getRandomDouble(double a, double b) {
    double r0 = (double)rand() / RAND_MAX;
    return a + r0 * (b - a);
}

int main() {
    srand(time(nullptr));
    Sample samplesTest[100];
    
    Sample sample1;
    Sample sample2(10.0, 10.0, 1);
    
    
    
    cin >> sample1;
    
    Classifier myClassifier;
    
    for (int i = 0; i < 1000; ++i) {
        double xVal = getRandomDouble(0.0, 100.0);
        double yVal = getRandomDouble(0.0, 100.0);
        int labelVal = rand() % 2;
        Sample s(xVal, yVal, labelVal);
        samples[i].setX(xVal);
        samples[i].setY(yVal);
        samples[i].setLabel(labelVal);
        
    }
    
    
    
    return 0;
}
