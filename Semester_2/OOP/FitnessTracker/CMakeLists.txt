cmake_minimum_required(VERSION 3.16)

project(FitnessTracker VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

qt_standard_project_setup(REQUIRES 6.8)

qt_add_executable(appFitnessTracker
    main.cpp
    Activity.h Activity.cpp
    User.h User.cpp
    BaseRepository.h BaseRepository.cpp
    CSVRepository.h CSVRepository.cpp
    JSONRepository.h JSONRepository.cpp
    Controller.h Controller.cpp
    Command.h Command.cpp
    ActivityFilter.h ActivityFilter.cpp
    mainwindow.h mainwindow.cpp
    Tests.h
)

set_target_properties(appFitnessTracker PROPERTIES
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE
    WIN32_EXECUTABLE
)

target_link_libraries(appFitnessTracker
    PRIVATE Qt6::Widgets
)

include(GNUInstallDirs)
install(TARGETS appFitnessTracker
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
