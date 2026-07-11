#include "mainwindow.h"
#include "Tests.h"
#include <QApplication>

int main(int argc, char *argv[]) {
    runAllTests();

    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
