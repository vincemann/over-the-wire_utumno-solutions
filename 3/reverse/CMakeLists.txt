cmake_minimum_required(VERSION 3.19)
project(reverse C)
project(program C)

set(CMAKE_C_STANDARD 99)

#SET(GCC_COVERAGE_COMPILE_FLAGS "-m32 -no-pie")
#add_definitions(${GCC_COVERAGE_COMPILE_FLAGS})
add_executable(reverse reverse.c)
add_executable(program program.c)

set_target_properties(program PROPERTIES COMPILE_FLAGS "-m32 -no-pie -fno-stack-protector" LINK_FLAGS "-m32 -no-pie -fno-stack-protector")
set_target_properties(reverse PROPERTIES COMPILE_FLAGS "-m32 -no-pie -fno-stack-protector"  LINK_FLAGS "-m32 -no-pie -fno-stack-protector")
#target_compile_options(program PRIVATE -m32 -no-pie)
#target_compile_options(reverse PRIVATE -m32 -no-pie)

