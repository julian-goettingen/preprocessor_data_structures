#if FORCE_C11_PRINT==1
#define C11_PRINT
#endif
#if FORCE_CXX_PRINT==1
#define CXX_PRINT
#endif
#if FORCE_DUMP_PRINT==1
#define DUMP_PRINT
#endif
#if FORCE_NO_PRINT==1
#define NO_PRINT
#endif



#if defined C11_PRINT
#include "c11_print_anything.h"
#elif defined DUMP_PRINT
#include "dump_print_anything.h"
#elif defined CXX_PRINT
#include "cxx_print_anything.h"
#elif defined NO_PRINT
#include "empty_print_definitions.h"
#else
#error "print_anything.h needs an implementation, choose one by defining one of the symbols before including it."
#endif
