cmake_minimum_required(VERSION 3.5)
project(runscripts LANGUAGES)

install(PROGRAMS plan.py run.py DESTINATION bin)

configure_file(config.cmake.in runscripts-config.cmake @ONLY)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/runscripts-config.cmake" DESTINATION cmake)
