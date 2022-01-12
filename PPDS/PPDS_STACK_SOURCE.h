#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

//#define FORCE_C11_PRINT
//#define FORCE_CXX_PRINT
//#define FORCE_DUMP_PRINT
//#define AUTO_PRINT

#define CXX_PRINT
#include "print_anything.h"


/* PPDS_SOURCE
{% set name, pointer, maxsize = args %}
{% set declare_site = declare_site %}
{% set size = name + "_size" %}


#define {{name}}_assert(expr,msg) (void)(expr?(void)0:({{name}}_assert_fail(expr,msg)))


#define {{name}}_PUSH(elem) do{ {{pointer}}[{{name}}_assert({{size}}<{{maxsize}},"max size reached, cant push more items"), {{size}}++] = (elem);}while(0)

#define {{name}}_POP() {{pointer}}[{{name}}_assert({{size}}>0,"cant pop from empty stack"), --{{size}}]

#define {{name}}_AT(i) {{pointer}}[{{name}}_assert(i>=0 && i<{{size}},"i=" #i "is out of bounds for the stack of size " {{size}}), {{size}}]

#define {{name}}_assert_fail(expr,msg) \
    fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE: %s <----\n", msg),\
    fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
    fprintf(stderr, "with the object {{name}} declared in {{declare_site}} of type STACK\n"),\
    fprintf(stderr, "object {{name}} defined by: size={{size}}, maxsize={{maxsize}}, pointer={{pointer}}\n"),\
    fprintf(stderr, "values of {{name}}:\n"), PRINT({{size}}), PRINT({{pointer}}), PRINT({{maxsize}}),\
    PRINT_ARR({{pointer}},{{size}}),\
    fprintf(stderr, #expr " evaluated to %d, exiting program.\n", expr),\
    exit(1)

*/


#define PPDS_DECLARE_STACK(name, pointer, maxsize) typeof(maxsize) name##_size = 0
