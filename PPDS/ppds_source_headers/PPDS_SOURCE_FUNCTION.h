


// definition is the whole definition/declaration of the function and gets special treatment.
// more properties will be generated from it in the object
/* PPDS_ARGS:
args:
    - func_name
    - definition
kwargs: {}
*/

//"\\s*PPDS_FUNCTION\\((.*)\\)(?=\s*[;)"
/* PPDS_CONSTRUCTORS:
 [
    "\\s*PPDS_FUNCTION(\\(.*)"
 ]
*/

/* PPDS_DEF:

////////////////////////////////////////
////// FUNCTION DEFINITION /////////////
// FROM: {{declare_site}}
////////////////////////////////////////

// your definition must be repeated here otherwise it cant properly be used below.
{{definition}};

// this function is a wrapper around your original function. python will call it
// nonnull char*-returns will be translated into exceptions
const char * {{func_name}}_4py( {% for arg in func_args_expanded_with_types %} {{arg}}{{", " if not loop.last else ""}}{% endfor %}) {
    {% for check in func_precon_checks %}
    {{check}}
    {% endfor %}
    return {{func_name}}( {% for arg in func_args_expanded_names%} {{arg}}{{", " if not loop.last else ""}}{% endfor %});
}

// this macro is designed as a wrapper around your function for use by c-code
#define {{func_name.upper()}}({% for arg in func_args_unexpanded_names%} {{arg}}{{", " if not loop.last else ""}}{% endfor %}) \
 {{func_name}}({% for arg in func_args_expanded_names %}{{arg}}{{", " if not loop.last else ""}}{% endfor %})


// end of function definition from {{declare_site}} ////
*/

/* PPDS_UNDEF:

// undef from function-definition at site {{declare_site}} intentionally empty

*/

// the original function-declaration will be replaced by the definition the user supplied
#define PPDS_FUNCTION(name, def) def

