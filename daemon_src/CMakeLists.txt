cmake_minimum_required(VERSION 3.31)
project(cputild)

set(CMAKE_CXX_STANDARD 26)

add_executable(cputild
    main.cpp
    lib_cputild.cpp
    lib_cputild.h
    string_utils.cpp
    string_utils.h
    utils.cpp
    utils.h
    Config.cpp
    Config.h
)