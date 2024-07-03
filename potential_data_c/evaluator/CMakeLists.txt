cmake_minimum_required(VERSION 3.14)

project(PokerHandEvaluator VERSION 0.6.0)

set(CMAKE_BUILD_TYPE  "Release")

# Use C++ 11 Standard to compile
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_C_STANDARD 99)

option(BUILD_CARD5 "Build 5-card standalone library" ON)
option(BUILD_CARD6 "Build 6-card standalone library" ON)
option(BUILD_CARD7 "Build 7-card standalone library" ON)

add_library(pheval SHARED 
  src/card_sampler.cc
  src/dptables.c
  src/evaluator5.cc
  src/evaluator5.c
  src/evaluator6.cc
  src/evaluator6.c
  src/evaluator7.cc
  src/evaluator7.c
  src/tables_bitwise.c
  src/hash.c
  src/hashtable.c
  src/hashtable5.c
  src/hashtable6.c
  src/hashtable7.c
  src/rank.c
  src/7462.c
)
target_include_directories(pheval PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include/>)
target_compile_options(pheval PUBLIC -O3 -fPIC)
set(PUB_HEADERS include/phevaluator/phevaluator.h
                include/phevaluator/card.h
                include/phevaluator/card_sampler.h
                include/phevaluator/rank.h)
set_target_properties(pheval PROPERTIES
    VERSION ${PROJECT_VERSION}
    PUBLIC_HEADER "${PUB_HEADERS}")

if (BUILD_CARD5)
  add_library(pheval5 SHARED
    src/dptables.c
    src/tables_bitwise.c
    src/evaluator5.c
    src/evaluator5.cc
    src/hashtable5.c
    src/hashtable.c
    src/hash.c
  )
  target_include_directories(pheval5 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(pheval5 PUBLIC -O3 -fPIC)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/rank.h)
  set_target_properties(pheval5 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_CARD6)
  add_library(pheval6 SHARED
    src/dptables.c
    src/tables_bitwise.c
    src/evaluator6.c
    src/evaluator6.cc
    src/hashtable6.c
    src/hashtable.c
    src/hash.c
  )
  target_include_directories(pheval6 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(pheval6 PUBLIC -O3 -fPIC)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/rank.h)
  set_target_properties(pheval6 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_CARD7)
  add_library(pheval7 SHARED
    src/dptables.c
    src/tables_bitwise.c
    src/evaluator7.c
    src/evaluator7.cc
    src/hashtable7.c
    src/hashtable.c
    src/hash.c
  )
  target_include_directories(pheval7 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(pheval7 PUBLIC -O3 -fPIC)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/rank.h)
  set_target_properties(pheval7 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

# Install library
if (UNIX)
  include(GNUInstallDirs)
  install(TARGETS pheval
      EXPORT phevalTargets
      LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
      PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)

  if (BUILD_PLO4)
    install(TARGETS phevalplo4
        EXPORT phevalTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)
  endif()

  if (BUILD_PLO5)
    install(TARGETS phevalplo5
        EXPORT phevalTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)
  endif()

  if (BUILD_PLO6)
    install(TARGETS phevalplo6
        EXPORT phevalTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)
  endif()

  #install find_package script
  install(EXPORT phevalTargets
    NAMESPACE phevaluator::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/phevaluator)

  include(CMakePackageConfigHelpers)

  configure_package_config_file(
          ${CMAKE_CURRENT_SOURCE_DIR}/phevaluatorConfig.cmake.in
          ${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfig.cmake
          INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/phevaluator
          PATH_VARS
          CMAKE_INSTALL_LIBDIR)

  write_basic_package_version_file(
          ${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfigVersion.cmake
          COMPATIBILITY SameMajorVersion)

  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfig.cmake"
          "${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfigVersion.cmake"
          DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/phevaluator")
endif()
