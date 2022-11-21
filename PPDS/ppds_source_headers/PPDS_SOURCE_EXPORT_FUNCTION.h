


// definition is the whole definition/declaration of the function and gets special treatment.
// more properties will be generated from it in the object
/* PPDS_ARGS:
{
 "args": [],
 "kwargs": {}
}
*/

/* PPDS_CONSTRUCTORS:
 [
    "\\s*PPDS_FUNCTION_(.*)\\(.*)"
 ]
*/

/* PPDS_DEF:

////////////////////////////////////////
////// FUNCTION DEFINITION /////////////
// FROM: {{declare_site}}
////////////////////////////////////////

// this function is a generated wrapper around your original code
// - it quits the program if arguments dont fit the requirements
{{func_name}}( {% for arg in func_arg_declarations %} {{arg}}  {% endfor %} ) {

    {{func_name}}_unsafe(
}


 //WIP



// the original function will be replaced
#define PPDS_FUNCTION_{{func_name}} {{func_decl_replacement}}
*/

