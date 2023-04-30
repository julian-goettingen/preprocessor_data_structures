#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include "print_anything.h"


/* PPDS_ARGS:
{
  "args": ["name", "arg1", "arg2"],
  "kwargs": {"skip_checks": "NDEBUG", "panic": "exit(1)", "print_base":"PRINT"}
}
*/

braucht Variable Zahl von Argumenten und muss die expansions benutzen können...

/* PPDS_DEF:
int {{name}}({{arg1}}, {{arg2}})
*/



