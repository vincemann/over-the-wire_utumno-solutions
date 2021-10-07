cmake_minimum_required(VERSION 3.19)
project(test C)

set(CMAKE_C_STANDARD 99)

add_executable(test main.c)

set_target_properties(test PROPERTIES COMPILE_FLAGS "-m32 -no-pie -fno-stack-protector" LINK_FLAGS "-m32 -no-pie -fno-stack-protector")
set_target_properties(test PROPERTIES COMPILE_FLAGS "-m32 -no-pie -fno-stack-protector"  LINK_FLAGS "-m32 -no-pie -fno-stack-protector")
#target_compile_options(program PRIVATE -m32 -no-pie)
#target_compile_options(reverse PRIVATE -m32 -no-pie)