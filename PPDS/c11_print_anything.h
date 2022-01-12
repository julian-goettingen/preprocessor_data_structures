#ifdef __cplusplus
#error cannot compile these C11-PRINT-macros with a c++ compiler, choose a different print method like None, CXX or dump
#include <this compilation stop saves you from many lines of error messages>
#endif

#include <stdio.h>
#include <math.h>
#include <limits.h>
#include <stdbool.h>

// draws inspiration and code from http://www.robertgamble.net/2012/01/c11-generic-selections.html

#define HAS_FORMATTER(x) _Generic((x), \
    char: 1, \
    signed char: 1, \
    unsigned char: 1, \
    signed short: 1, \
    unsigned short: 1, \
    signed int: 1, \
    unsigned int: 1, \
    long int: 1, \
    unsigned long int: 1, \
    long long int: 1, \
    unsigned long long int: 1, \
    float: 1, \
    double: 1, \
    long double: 1, \
\
    const char *: 1, \
    char *: 1, \
\
    unsigned char *: 1, \
    short int *: 1, \
    unsigned short int *: 1, \
    int *: 1, \
    unsigned int *: 1, \
    long int *: 1, \
    unsigned long int *: 1, \
    long long int *: 1, \
    unsigned long long int *: 1, \
    float *: 1, \
    double *: 1, \
    long double *: 1, \
\
    char * *: 1, \
    signed char * *: 1, \
    unsigned char * *: 1, \
    short int * *: 1, \
    unsigned short int * *: 1, \
    int * *: 1, \
    unsigned int * *: 1, \
    long int * *: 1, \
    unsigned long int * *: 1, \
    long long int * *: 1, \
    unsigned long long int * *: 1, \
    float * *: 1, \
    double * *: 1, \
    long double * *: 1, \
\
    char * * *: 1, \
    signed char * * *: 1, \
    unsigned char * * *: 1, \
    short int * * *: 1, \
    unsigned short int * * *: 1, \
    int * * *: 1, \
    unsigned int * * *: 1, \
    long int * * *: 1, \
    unsigned long int * * *: 1, \
    long long int * * *: 1, \
    unsigned long long int * * *: 1, \
    float * * *: 1, \
    double * * *: 1, \
    long double * * *: 1, \
\
    const unsigned char *: 1, \
    const short int *: 1, \
    const unsigned short int *: 1, \
    const int *: 1, \
    const unsigned int *: 1, \
    const long int *: 1, \
    const unsigned long int *: 1, \
    const long long int *: 1, \
    const unsigned long long int *: 1, \
    const float *: 1, \
    const double *: 1, \
    const long double *: 1, \
\
    const char * *: 1, \
    const signed char * *: 1, \
    const unsigned char * *: 1, \
    const short int * *: 1, \
    const unsigned short int * *: 1, \
    const int * *: 1, \
    const unsigned int * *: 1, \
    const long int * *: 1, \
    const unsigned long int * *: 1, \
    const long long int * *: 1, \
    const unsigned long long int * *: 1, \
    const float * *: 1, \
    const double * *: 1, \
    const long double * *: 1, \
\
    const char * * *: 1, \
    const signed char * * *: 1, \
    const unsigned char * * *: 1, \
    const short int * * *: 1, \
    const unsigned short int * * *: 1, \
    const int * * *: 1, \
    const unsigned int * * *: 1, \
    const long int * * *: 1, \
    const unsigned long int * * *: 1, \
    const long long int * * *: 1, \
    const unsigned long long int * * *: 1, \
    const float * * *: 1, \
    const double * * *: 1, \
    const long double * * *: 1, \
\
    void *: 1, \
    void **: 1,\
    void ***: 1,\
    default: 0)

#define FORMATTER(x) _Generic((x), \
    char: "%c", \
    signed char: "%hhd", \
    unsigned char: "%hhu", \
    signed short: "%hd", \
    unsigned short: "%hu", \
    signed int: "%d", \
    unsigned int: "%u", \
    long int: "%ld", \
    unsigned long int: "%lu", \
    long long int: "%lld", \
    unsigned long long int: "%llu", \
    float: "%f", \
    double: "%f", \
    long double: "%Lf", \
\
    const char *: "%s", \
    char *: "%s", \
\
    unsigned char *: "%p", \
    short int *: "%p", \
    unsigned short int *: "%p", \
    int *: "%p", \
    unsigned int *: "%p", \
    long int *: "%p", \
    unsigned long int *: "%p", \
    long long int *: "%p", \
    unsigned long long int *: "%p", \
    float *: "%p", \
    double *: "%p", \
    long double *: "%p", \
\
    char * *: "%p", \
    signed char * *: "%p", \
    unsigned char * *: "%p", \
    short int * *: "%p", \
    unsigned short int * *: "%p", \
    int * *: "%p", \
    unsigned int * *: "%p", \
    long int * *: "%p", \
    unsigned long int * *: "%p", \
    long long int * *: "%p", \
    unsigned long long int * *: "%p", \
    float * *: "%p", \
    double * *: "%p", \
    long double * *: "%p", \
\
    char * * *: "%p", \
    signed char * * *: "%p", \
    unsigned char * * *: "%p", \
    short int * * *: "%p", \
    unsigned short int * * *: "%p", \
    int * * *: "%p", \
    unsigned int * * *: "%p", \
    long int * * *: "%p", \
    unsigned long int * * *: "%p", \
    long long int * * *: "%p", \
    unsigned long long int * * *: "%p", \
    float * * *: "%p", \
    double * * *: "%p", \
    long double * * *: "%p", \
\
    const unsigned char *: "%p", \
    const short int *: "%p", \
    const unsigned short int *: "%p", \
    const int *: "%p", \
    const unsigned int *: "%p", \
    const long int *: "%p", \
    const unsigned long int *: "%p", \
    const long long int *: "%p", \
    const unsigned long long int *: "%p", \
    const float *: "%p", \
    const double *: "%p", \
    const long double *: "%p", \
\
    const char * *: "%p", \
    const signed char * *: "%p", \
    const unsigned char * *: "%p", \
    const short int * *: "%p", \
    const unsigned short int * *: "%p", \
    const int * *: "%p", \
    const unsigned int * *: "%p", \
    const long int * *: "%p", \
    const unsigned long int * *: "%p", \
    const long long int * *: "%p", \
    const unsigned long long int * *: "%p", \
    const float * *: "%p", \
    const double * *: "%p", \
    const long double * *: "%p", \
\
    const char * * *: "%p", \
    const signed char * * *: "%p", \
    const unsigned char * * *: "%p", \
    const short int * * *: "%p", \
    const unsigned short int * * *: "%p", \
    const int * * *: "%p", \
    const unsigned int * * *: "%p", \
    const long int * * *: "%p", \
    const unsigned long int * * *: "%p", \
    const long long int * * *: "%p", \
    const unsigned long long int * * *: "%p", \
    const float * * *: "%p", \
    const double * * *: "%p", \
    const long double * * *: "%p", \
\
    void *: "%p", \
    void **: "%p",\
    void ***: "%p")

/* Get the name of a type */
#define TYPE_NAME(x) _Generic((x), _Bool: "_Bool", \
\
    char: "char", \
    signed char: "signed char", \
    unsigned char: "unsigned char", \
    short int: "short int", \
    unsigned short int: "unsigned short int", \
    int: "int", \
    unsigned int: "unsigned int", \
    long int: "long int", \
    unsigned long int: "unsigned long int", \
    long long int: "long long int", \
    unsigned long long int: "unsigned long long int", \
    float: "float", \
    double: "double", \
    long double: "long double", \
\
    char *: "char *", \
    signed char *: "signed char *", \
    unsigned char *: "unsigned char *", \
    short int *: "short int *", \
    unsigned short int *: "unsigned short int *", \
    int *: "int *", \
    unsigned int *: "unsigned int *", \
    long int *: "long int *", \
    unsigned long int *: "unsigned long int *", \
    long long int *: "long long int *", \
    unsigned long long int *: "unsigned long long int *", \
    float *: "float *", \
    double *: "double *", \
    long double *: "long double *", \
\
    char * *: "char * *", \
    signed char * *: "signed char * *", \
    unsigned char * *: "unsigned char * *", \
    short int * *: "short int * *", \
    unsigned short int * *: "unsigned short int * *", \
    int * *: "int * *", \
    unsigned int * *: "unsigned int * *", \
    long int * *: "long int * *", \
    unsigned long int * *: "unsigned long int * *", \
    long long int * *: "long long int * *", \
    unsigned long long int * *: "unsigned long long int * *", \
    float * *: "float * *", \
    double * *: "double * *", \
    long double * *: "long double * *", \
\
    char * * *: "char * * *", \
    signed char * * *: "signed char * * *", \
    unsigned char * * *: "unsigned char * * *", \
    short int * * *: "short int * * *", \
    unsigned short int * * *: "unsigned short int * * *", \
    int * * *: "int * * *", \
    unsigned int * * *: "unsigned int * * *", \
    long int * * *: "long int * * *", \
    unsigned long int * * *: "unsigned long int * * *", \
    long long int * * *: "long long int * * *", \
    unsigned long long int * * *: "unsigned long long int * * *", \
    float * * *: "float * * *", \
    double * * *: "double * * *", \
    long double * * *: "long double * * *", \
\
    const char *: "const char *", \
    const signed char *: "const signed char *", \
    const unsigned char *: "const unsigned char *", \
    const short int *: "const short int *", \
    const unsigned short int *: "const unsigned short int *", \
    const int *: "const int *", \
    const unsigned int *: "const unsigned int *", \
    const long int *: "const long int *", \
    const unsigned long int *: "const unsigned long int *", \
    const long long int *: "const long long int *", \
    const unsigned long long int *: "const unsigned long long int *", \
    const float *: "const float *", \
    const double *: "const double *", \
    const long double *: "const long double *", \
\
    const char * *: "const char * *", \
    const signed char * *: "const signed char * *", \
    const unsigned char * *: "const unsigned char * *", \
    const short int * *: "const short int * *", \
    const unsigned short int * *: "const unsigned short int * *", \
    const int * *: "const int * *", \
    const unsigned int * *: "const unsigned int * *", \
    const long int * *: "const long int * *", \
    const unsigned long int * *: "const unsigned long int * *", \
    const long long int * *: "const long long int * *", \
    const unsigned long long int * *: "const unsigned long long int * *", \
    const float * *: "const float * *", \
    const double * *: "const double * *", \
    const long double * *: "const long double * *", \
\
    const char * * *: "const char * * *", \
    const signed char * * *: "const signed char * * *", \
    const unsigned char * * *: "const unsigned char * * *", \
    const short int * * *: "const short int * * *", \
    const unsigned short int * * *: "const unsigned short int * * *", \
    const int * * *: "const int * * *", \
    const unsigned int * * *: "const unsigned int * * *", \
    const long int * * *: "const long int * * *", \
    const unsigned long int * * *: "const unsigned long int * * *", \
    const long long int * * *: "const long long int * * *", \
    const unsigned long long int * * *: "const unsigned long long int * * *", \
    const float * * *: "const float * * *", \
    const double * * *: "const double * * *", \
    const long double * * *: "const long double * * *", \
\
    void *: "void *", \
    void **: "void **",\
    void ***: "void ***",\
    default: "other")

#define PRINT(x) fprintf(stderr,"( "),\
    fprintf(stderr,TYPE_NAME(x)),\
    fprintf(stderr," "),\
    fprintf(stderr,#x),\
    fprintf(stderr," = "),\
    fprintf(stderr,FORMATTER(x), x),\
    fprintf(stderr," )")


#define PRINT_ARRAY_ELEMENTS(x,n) ((void)_Generic((x),\
\
    double*: print_double_arr, \
    const double*: print_double_arr, \
    float *: print_float_arr, \
    const float*: print_float_arr,\
    long double*: print_long_double_arr,\
    const long double*: print_long_double_arr,\
\
    int*: print_int_arr,\
    const int*: print_int_arr,\
    short*: print_short_arr,\
    const short*: print_short_arr,\
    signed char*: print_signed_char_arr,\
    const signed char*: print_signed_char_arr,\
    long*: print_long_arr,\
    const long*: print_long_arr,\
    long long*: print_long_long_arr,\
    const long long*: print_long_long_arr,\
\
    unsigned int*: print_unsigned_int_arr,\
    const unsigned int*: print_unsigned_int_arr,\
    unsigned short*: print_unsigned_short_arr,\
    const unsigned short*: print_unsigned_short_arr,\
    unsigned char*: print_unsigned_char_arr,\
    const unsigned char*: print_unsigned_char_arr,\
    unsigned long*: print_unsigned_long_arr,\
    const unsigned long*: print_unsigned_long_arr,\
    unsigned long long*: print_unsigned_long_long_arr,\
    const unsigned long long*: print_unsigned_long_long_arr,\
\
    default: unable_to_print_arr\
)(x,n))


/*inline*/ /*static*/ void unable_to_print_arr(const void * x, size_t n) {
    (void) x;
    (void) n;
    fprintf(stderr,"...unable to print array content. Unusual datatype?\n");
}

/*inline*/ /*static*/ void print_human_readable_number_desc(size_t value, size_t max_val, const char* desc){
    if (value == max_val) {
        fprintf(stderr,"ALL are ");
    }
    else if (value == 0) {
        fprintf(stderr,"None are ");
    }
    else {
        fprintf(stderr,"%zu/%zu are ", value, max_val);
    }
    fputs(desc, stderr); //fputs rather than printf avoids a warning with clang bc it considers the case where desc has format specifiers
    fprintf(stderr,"; ");
}

/*inline*/ /*static*/ void print_magnitude_summary(size_t n_positive, size_t n_zero, size_t n_negative, size_t n) {
    if (n_zero == n) {
        fprintf(stderr,"All values are zero");
    }
    else if (n_positive == n) {
        fprintf(stderr,"All values are positive");
    }
    else if (n_negative == n) {
        fprintf(stderr,"All values are negative");
    }
    else if (n_negative + n_zero == n) {
        fprintf(stderr,"All values are non-positive (%zu are negative)", n_negative);
    }
    else if (n_positive + n_zero == n) {
        fprintf(stderr,"All values are non-negative (%zu are positive)", n_positive);
    }
    else {
        fprintf(stderr,"%zu are positive, %zu are zero, %zu are negative", n_positive, n_zero, n_negative);
    }
}


#define DEFINE_FLOATY_PRINT_ARR(function_name, float_type) \
/*inline*/ /*static*/ void function_name(const float_type *x, size_t n) {\
    /* display all values if n<=cutoff */\
    const unsigned cutoff = 20;\
    /* display first and last n_show values if n>cutoff*/\
    const unsigned n_show = 6;\
\
    if ( n > cutoff ) {\
        size_t n_nans = 0;\
        size_t n_finite = 0;\
        size_t n_positive = 0;\
        size_t n_zero = 0;\
        size_t n_negative = 0;\
        size_t n_normal = 0;\
        float_type maxval = x[0];\
        float_type minval = x[0];\
        long double sum = 0;\
\
        fprintf(stderr,"[");\
        for (size_t i=0; i<n; i++) {\
\
            if (i<n_show || n-i-1<n_show) {\
                fprintf(stderr,"%lf",(double)x[i]);\
                if (i!=n-1) {\
                    fprintf(stderr,", ");\
                }\
            }\
            if (i==n_show) {\
                fprintf(stderr," ... ");\
            }\
            \
            if (isnan(x[i])) n_nans++;\
            if (isfinite(x[i])) n_finite++;\
            if (x[i] > 0) n_positive++;\
            if (x[i] == 0) n_zero++;\
            if (x[i] < 0) n_negative++;\
            if (isnormal(x[i])) n_normal++;\
            if (x[i] > maxval) maxval=x[i];\
            if (x[i] < minval) minval=x[i];\
            sum += x[i];\
        }\
        fprintf(stderr,"]\n");\
\
        print_human_readable_number_desc(n_nans, n, "NaN");\
        print_human_readable_number_desc(n_finite, n, "finite");\
        print_human_readable_number_desc(n_normal, n, "normal");\
        fprintf(stderr,"\n");\
        print_magnitude_summary(n_positive, n_zero, n_negative, n);\
        fprintf(stderr,"\nValues range from %lf to %lf with an average of %lf\n", (double)minval, (double)maxval, (double)(sum/n));\
    }\
    else /* only a few values, just print all*/ {\
        fprintf(stderr,"[");\
        for (size_t i=0; i<n; i++) {\
\
            fprintf(stderr,"%lf",(double)x[i]);\
            if (i!=n-1) {\
                fprintf(stderr,", ");\
            }\
        } \
        fprintf(stderr,"]\n");\
    }\
}\

DEFINE_FLOATY_PRINT_ARR(print_double_arr, double)
DEFINE_FLOATY_PRINT_ARR(print_long_double_arr, long double);
DEFINE_FLOATY_PRINT_ARR(print_float_arr, float);


#define DEFINE_SIGNED_PRINT_ARR(name, int_type, int_max, int_min) \
/*inline*/ /*static*/ void name( int_type *x, size_t n) {\
\
     /* display all values if n<=cutoff */\
    const unsigned cutoff = 20;\
    /* display first and last n_show values if n>cutoff*/\
    const unsigned n_show = 6;\
\
    if ( n > cutoff ){\
        size_t n_positive = 0;\
        size_t n_negative = 0;\
        size_t n_zero = 0;\
        size_t n_high = 0;\
        size_t n_low = 0;\
        size_t n_minus_one = 0;\
        int_type minval = x[0];\
        int_type maxval = x[0];\
        long double sum = 0;\
        double high = int_max/2;\
        double low = int_min/2;\
\
        fprintf(stderr,"[");\
        for (size_t i=0; i<n; i++) {\
            if (i<n_show || n-i-1<n_show) {\
                fprintf(stderr,"%lld",(long long)x[i]);\
                if (i!=n-1) {\
                    fprintf(stderr,", ");\
                }\
            }\
            if (i==n_show) {\
                fprintf(stderr," ... ");\
            }\
\
            if (x[i] > 0) n_positive++;\
            if (x[i] < 0) n_negative++;\
            if (x[i] == 0) n_zero++;\
            if (x[i] > high) n_high++;\
            if (x[i] < low) n_low++;\
            if (x[i] == -1) n_minus_one++;\
            if (x[i] > maxval) maxval=x[i];\
            if (x[i] < minval) minval=x[i];\
            sum += x[i];\
        }\
\
        fprintf(stderr,"]\n");\
        if (n_minus_one > 0) {\
            print_human_readable_number_desc(n_minus_one, n, "-1");\
            fprintf(stderr,"\n");\
        }\
        print_magnitude_summary(n_positive, n_zero, n_negative, n);\
        if (n_high+n_low > 0) {\
            fprintf(stderr,"consider danger of overflow? --> ");\
            print_human_readable_number_desc(n_high, n, "> dtype_max_value/2");\
            print_human_readable_number_desc(n_low, n, "< dtype_min_value/2");\
            fprintf(stderr,"\n");\
        }\
        else {\
            fprintf(stderr,"all values in range [dtype_min_value/2, dtype_max_value/2]'\n");\
        }\
        fprintf(stderr,"\nValues range from %lf to %lf with an average of %lf\n", (double)minval, (double)maxval, (double)(sum/n));\
    }\
    else /* only a few values, just print all*/ {\
        fprintf(stderr,"[");\
        for (size_t i=0; i<n; i++) {\
\
            fprintf(stderr,"%lld",(long long)x[i]);\
            if (i!=n-1) {\
                fprintf(stderr,", ");\
            }\
        } \
        fprintf(stderr,"]\n");\
    }\
}

DEFINE_SIGNED_PRINT_ARR(print_int_arr, int, INT_MAX, INT_MIN);
DEFINE_SIGNED_PRINT_ARR(print_long_arr, long, LONG_MAX, LONG_MIN);
DEFINE_SIGNED_PRINT_ARR(print_long_long_arr, long long, LLONG_MAX, LLONG_MIN);
DEFINE_SIGNED_PRINT_ARR(print_short_arr, short, SHRT_MAX, SHRT_MIN);
DEFINE_SIGNED_PRINT_ARR(print_char_arr, char, CHAR_MAX, CHAR_MIN);
DEFINE_SIGNED_PRINT_ARR(print_signed_char_arr, signed char, SCHAR_MAX, SCHAR_MIN);

#define DEFINE_UNSIGNED_PRINT_ARR(name, uint_type, uint_max) \
/*inline*/ /*static*/ void name( uint_type *x, size_t n) {\
\
     /* display all values if n<=cutoff */\
    const unsigned cutoff = 20;\
    /* display first and last n_show values if n>cutoff*/\
    const unsigned n_show = 6;\
\
    if ( n > cutoff ){\
        size_t n_positive = 0;\
        size_t n_zero = 0;\
        size_t n_high = 0;\
        size_t n_uint_max = 0;\
        uint_type minval = x[0];\
        uint_type maxval = x[0];\
        long double sum = 0;\
        double high = uint_max/2;\
\
        fprintf(stderr,"[");\
        for (size_t i=0; i<n; i++) {\
            if (i<n_show || n-i-1<n_show) {\
                fprintf(stderr,"%lld",(unsigned long long)x[i]);\
                if (i!=n-1) {\
                    fprintf(stderr,", ");\
                }\
            }\
            if (i==n_show) {\
                fprintf(stderr," ... ");\
            }\
\
            if (x[i] > 0) n_positive++;\
            if (x[i] == 0) n_zero++;\
            if (x[i] == uint_max) n_uint_max++;\
            if (x[i] > high) n_high++;\
            if (x[i] > maxval) maxval=x[i];\
            if (x[i] < minval) minval=x[i];\
            sum += x[i];\
        }\
\
        fprintf(stderr,"]\n");\
        if (n_uint_max > 0) {\
            print_human_readable_number_desc(n_uint_max , n, "Maximum value for the uint-type");\
            fprintf(stderr,"\n");\
        }\
        print_human_readable_number_desc(n_high, n, "higher than dtype_max_value/2");\
        if (n_zero == n){\
            fprintf(stderr,"all values are zero");\
        }\
        else if (n_positive == n){\
            fprintf(stderr,"all values are >0");\
        }\
        else {\
            fprintf(stderr,"%zu positive values, %zu zeroes", n_positive, n_zero);\
        }\
        fprintf(stderr,"\n");\
        if (n_high > 0) {\
            fprintf(stderr,"consider danger of overflow? --> ");\
            print_human_readable_number_desc(n_high, n, "> dtype_max_value/2");\
            fprintf(stderr,"\n");\
        }\
        else {\
            fprintf(stderr,"all values in range [0, dtype_max_value/2]'\n");\
        }\
        fprintf(stderr,"\nValues range from %lf to %lf with an average of %lf\n", (double)minval, (double)maxval, (double)(sum/n));\
    }\
    else /* only a few values, just print all*/ {\
        fprintf(stderr,"[");\
        for (size_t i=0; i<n; i++) {\
\
            fprintf(stderr,"%lld",(long long)x[i]);\
            if (i!=n-1) {\
                fprintf(stderr,", ");\
            }\
        } \
        fprintf(stderr,"]\n");\
    }\
}

DEFINE_UNSIGNED_PRINT_ARR(print_unsigned_int_arr, unsigned int, UINT_MAX);
DEFINE_UNSIGNED_PRINT_ARR(print_unsigned_long_arr, unsigned long, ULONG_MAX);
DEFINE_UNSIGNED_PRINT_ARR(print_unsigned_long_long_arr, unsigned long long, ULLONG_MAX);
DEFINE_UNSIGNED_PRINT_ARR(print_unsigned_short_arr, unsigned short, USHRT_MAX);
DEFINE_UNSIGNED_PRINT_ARR(print_unsigned_char_arr, unsigned char, UCHAR_MAX);

// this unfortunately has the PRINT-macro copied into it,
// this is necessary so that #x, #n expands to the argument-name of PRINT_ARR, not to "x" or "n"
#define PRINT_ARR(x,n) \
    fprintf(stderr,"( "),\
    fprintf(stderr,TYPE_NAME(x)),\
    fprintf(stderr," "),\
    fprintf(stderr,#x),\
    fprintf(stderr," = "),\
    fprintf(stderr,FORMATTER(x), x),\
    fprintf(stderr," )"),\
    fprintf(stderr," is an array of size "),\
    fprintf(stderr,"( "),\
    fprintf(stderr,TYPE_NAME(n)),\
    fprintf(stderr," "),\
    fprintf(stderr,#n),\
    fprintf(stderr," = "),\
    fprintf(stderr,FORMATTER(n), n),\
    fprintf(stderr," )"),\
    fprintf(stderr," content: \n (element type: "),\
    fprintf(stderr,TYPE_NAME(x[0])),\
    fprintf(stderr,") "),\
    PRINT_ARRAY_ELEMENTS(x,n)


