#include <iostream>
#include <math.h>
#include <stdlib.h>

using namespace std;

class Point2D {
private:
  double x;
  double y;

public:
  Point2D(): x(0.0), y(0.0) {}
  Point2D(double xVal, double yVal): x(xVal), y(yVal) {}

  double getX() {
    return x;
  }

  double getY() {
    return y;
  }

  void setX(double val) {
    x = val;
  }

  void setY(double val) {
    y = val;
  }

  Point2D(const Point2D& other) {
    x = other.x;
    y = other.y;
  }

  Point2D& operator=(const Point2D& other) {
    if (this != &other) {
      x = other.x;
      y = other.y;
    }
    return *this;
  }

  friend ostream& operator<<(ostream& os, const Point2D& point) {
    os << "Point: (" << point.x << ", " << point.y << ")";
    return os;
  }

  friend istream& operator>>(istream& is, Point2D& point) {
    cout << "Enter the x coordinate: ";
    is >> point.x;
    cout << "\nEnter the y coordinate: ";
    is >> point.y;
    return is;
  }

  static double distanceToLine(Point2D point, double a, double b, double c) {
    double num1 = (double) fabs(a * point.x + b * point.y + c), num2 = sqrt(a * a + b * b);
    if (num2 == 0) {
      return 1e9;
    }
    double distance = num1 / num2;
    return distance;
  }

  friend Point2D operator-(Point2D a, Point2D b) {
    return Point2D(a.x - b.x, a.y - b.y);
  }

  bool operator!=(Point2D other) {
    return (this->x != other.x) || (this->y != other.y);
  }


  ~Point2D() {

  }
};

class RANSAC {
private:
  static Point2D points[2000];
  static int bestInliers;
  static double bestA, bestB, bestC;

public:
  static void setPoint(int index, Point2D point) {
    if (index >= 0 && index < 2000) {
      points[index] = point;
    }
  }

  static void reset() {
    bestInliers = 0;
    bestA = 0.0;
    bestB = 0.0;
    bestC = 0.0;
  }

  static void printResults() {
    cout << "The results of the RANSAC algorithm:\n" << "The inlier count is: " << bestInliers << "\nThe  coefficients are: "
    << bestA << " " << bestB << " " << bestC << "\n";
  }

  static void run(int iterations, double threshold) {
    bestInliers = 0;
    bestA = 0.0;
    bestB = 0.0;
    bestC = 0.0;
    for (int i = 0; i < iterations; ++i) {
      int index1 = rand() % 2000, index2 = rand() % 2000;
      Point2D p1 = points[index1], p2 = points[index2];
      double x1 = p1.getX(), y1 = p1.getY(), x2 = p2.getX(), y2 = p2.getY();
      double a = y2 - y1, b = x1 - x2, c = x2 * y1 - x1 * y2;
      if (a == 0 && b == 0) {
        continue;
      }
      int count = 0;
      for (int j = 0; j < 2000; ++j) {
        double dist = Point2D::distanceToLine(points[j], a, b, c);
        if (dist <= threshold) {
          ++count;
        }
      }
      if (count > bestInliers) {
        bestInliers = count;
        bestA = a, bestB = b, bestC = c;
      }
    }
  }

  ~RANSAC() {

  }
};

Point2D RANSAC::points[2000]; 
int RANSAC::bestInliers = 0;
double RANSAC::bestA = 0.0;
double RANSAC::bestB = 0.0;
double RANSAC::bestC = 0.0;

int main() {
  srand(time(nullptr));
  Point2D point1;
  Point2D* point2 = new Point2D(2.0, 4.0);
  cout << "Read point1: \n";
  cin >> point1;
  Point2D diffPoint = point1 - *point2;
  cout << "Result point of the difference: \n" << diffPoint;
  cout << "\n";
  RANSAC myRansac;

  
  for (int i = 0; i < 2000; ++i) {
    double xVal = (double) i;
    double yVal = (double) (xVal + (rand() % 100) / 50.0);
    Point2D pointI(xVal, yVal);
    myRansac.setPoint(i, pointI);
  }
  
  myRansac.run(100, 0.5);

  myRansac.printResults();

  delete point2;
  return 0;
}