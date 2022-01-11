#if defined C11_PRINT
#include "c11_print_anything.h"
#elif defined DUMP_PRINT
#include "dump_print_anything.h"
#elif defined CXX_PRINT
#include "cxx_print_anything.h"
#elif defined NO_PRINT
#include "empty_print_definitions.h"
#else
#error "print_anything.h needs an implementation"
#endif
