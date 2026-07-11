#include "mainwindow.h"
#include "SongController.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    SongController controller;
    MainWindow w(&controller);

    w.show();
    return a.exec();
}
