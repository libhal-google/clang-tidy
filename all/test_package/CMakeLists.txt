cmake_minimum_required(VERSION 3.15)

project(test_package LANGUAGES CXX)

add_executable(${PROJECT_NAME} main.cpp)

# Check if clang-tidy exists on the system and if so, evaluate each file
# against
find_program(CLANG_TIDY_EXE NAMES "clang-tidy")

# If ti exists, add it as an additional check for each source file
if(DEFINED CLANG_TIDY_EXE)
  message(STATUS "libhal[unit test]: Using clang-tidy")
  set(CONFIG_FILE_PATH "${CMAKE_SOURCE_DIR}/clang-tidy.conf")
  set(CLANG_TIDY "${CLANG_TIDY_EXE}" "--config-file=${CONFIG_FILE_PATH}")
  set_target_properties(${PROJECT_NAME} PROPERTIES CXX_CLANG_TIDY
    "${CLANG_TIDY}")
else()
  message(FATAL_ERROR "'clang-tidy' not available!")
endif(DEFINED CLANG_TIDY_EXE)
