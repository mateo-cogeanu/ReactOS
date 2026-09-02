/*
 * Compatibility declarations required by recent MinGW libstdc++ headers.
 * This file is force-included for C++ translation units by gcc.cmake.
 */

#pragma once

#if defined(__cplusplus) && (__cplusplus >= 201103L)
extern "C" int at_quick_exit(void (*)(void));
extern "C" __attribute__((noreturn)) void quick_exit(int);
#endif
