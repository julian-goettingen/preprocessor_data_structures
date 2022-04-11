#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define FORCE_CXX_PRINT 1
//#define FORCE_CXX_PRINT
//#define FORCE_DUMP_PRINT
//#define AUTO_PRINT
#include "print_anything.h"

// A PPDS_SOURCE header has 4 parts:
// the normal c/cpp-style header, that defines one special macro: PPDS_DECLARE_<name>(args)
// the PPDS_DECLARE-macro has positional must-have arguments and after that optional keyword-arguments
// PPDS_KW_DEFAULTS defines all possible keyword-arguments with their default values
// note that everything is a string
// example: PPDS_DECLARE_THING(AC,nx,ny,8,bound_check=1)
// 
// For each DECLARE, the templates PPDS_DEF and PPDS_UNDEF get instantiated with the following arguments:
// declare_site: a human-readable description of where the DECLARE happened
// args: the positional must-have args as a list
// kwargs: an object containing all optional keyword-arguments: either the default-value or the declared value
// jinja-tipps:
// kwargs values can be accessed with dot-notation: kwargs.value
// args values can be accessed by unpacking and putting into names: name, pointer, nx,ny,nz = args
//


// the notation of the keyword-defaults is yaml, though there is no nesting
/* PPDS_KW_DEFAULTS:
bounds_check_cond: 1
# yaml has comments like this
*/

// this gets put into the 
/* PPDS_DEF:
{% set name, pointer, maxsize = args %}
{% set bounds_check_cond
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
/* PPDS_UNDEF:
{% set name, pointer, maxsize = args}
#undef {{name}}_assert
#undef {{name}}_PUSH
#undef {{name}}_POP
#undef {{name}}_AT
#undef {{name}}_assert_fail
*/

#define PPDS_DECLARE_STACK(name, pointer, maxsize) typeof(maxsize) name##_size = 0

