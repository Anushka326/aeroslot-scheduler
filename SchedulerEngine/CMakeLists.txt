cmake_minimum_required(VERSION 3.14)
project(AirportSchedulerEngine CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# Gather source files (will be populated as implementation continues)
file(GLOB_RECURSE SRC_FILES "src/*.cpp")

# If no sources yet, provide a dummy to prevent errors, otherwise build the static library
if(SRC_FILES)
    add_library(SchedulerEngineCore STATIC ${SRC_FILES})
else()
    add_library(SchedulerEngineCore STATIC include/Flight.h) 
endif()
