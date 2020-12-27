cmake_minimum_required(VERSION 3.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

if(APPLE)
  set(basePoint @loader_path)
else()
  set(basePoint $ORIGIN)
endif()

set(CMAKE_BUILD_WITH_INSTALL_RPATH ON)

file(RELATIVE_PATH relDir
  ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}
  ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})

set(CMAKE_INSTALL_RPATH ${basePoint} ${basePoint}/${relDir})

add_executable(openvdb_test main.cpp)
target_link_libraries(openvdb_test ${CONAN_LIBS})
