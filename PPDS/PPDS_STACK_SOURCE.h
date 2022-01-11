#include <assert.h>
#include <stdio.h>
#include <stdlib.h>



// this can sort-of print anything, but if there is an alternative we should use that alternative
#define ERRPRINT_WILD(x) FPRINT_WILD(stderr,x)
#define FPRINT_WILD(f,x) fprint_wild(f,#x,&x,sizeof(x))
static inline void fprint_wild(FILE *f, const char* name, void *p, size_t size);
static inline void fprint_wild(FILE *f, const char* name, void *p, size_t size) {
    assert(p);
    assert(name);
    fprintf(f,"(%s [hex dump of %ld bytes]::", name, size);
    const unsigned char *c = (const unsigned char *) p;
    for (size_t i=0; i<size; i++){
        fprintf(f, " %02x", c[i]);
    }
    fprintf(f,")\n");
}



/* PPDS_SOURCE
{% set name, pointer, maxsize = args %}
{% set declare_site = declare_site %}
{% set size = name + "_size" %}


#define {{name}}_assert(expr,msg) (void)(expr?(void)0:({{name}}_assert_fail(expr,msg)))


#define {{name}}_PUSH(elem) do{ {{pointer}}[{{name}}_assert({{size}}<{{maxsize}},"max size reached, cant push more items"), {{size}}++] = (elem);}while(0)

#define {{name}}_POP() {{pointer}}[{{name}}_assert({{size}}>0,"cant pop from empty stack"), --{{size}}]

#define {{name}}_AT(i) {{pointer}}[{{name}}_assert(i>=0 && i<{{size}},"i=" #i "is out of bounds for the stack of size " {{size}}), {{size}}]

#define {{name}}_assert_fail(expr,msg) \
    fprintf(stderr,"\n\n----> ppds ASSERTION FAILURE with the object {{name}} (declared in {{declare_site}})\n"),\
    fprintf(stderr,"detected in line %d, func %s, file %s\n",__LINE__,__func__,__FILE__),\
    fprintf(stderr, "object {{name}} defined by: size={{size}}, maxsize={{maxsize}}, pointer={{pointer}}\n"),\
    fprintf(stderr, "hex dumps of values in preprocessor-object {{name}}:\n"), ERRPRINT_WILD({{size}}), ERRPRINT_WILD({{pointer}}), ERRPRINT_WILD({{maxsize}}),\
    fprintf(stderr,msg),\
    fprintf(stderr,"\n" #expr " evaluated to %d, exiting program.\n", expr),\
    exit(1)

*/


#define PPDS_DECLARE_STACK(name, pointer, maxsize) typeof(maxsize) name##_size = 0
