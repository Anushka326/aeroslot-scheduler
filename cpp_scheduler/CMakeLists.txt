cmake_minimum_required(VERSION 3.14)
project(AirportScheduler VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set strictly the include directories linking headers correctly
include_directories(include)

# Find source files for the standalone executable. Pybind bindings are built
# separately when pybind11 is available, so they are excluded from this target.
file(GLOB_RECURSE SRC_FILES src/*.cpp)
list(FILTER SRC_FILES EXCLUDE REGEX ".*bindings\\.cpp$")

# Generate explicit Executable
add_executable(airport_scheduler ${SRC_FILES})
