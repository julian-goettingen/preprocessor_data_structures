#include <stdio.h>
#include <math.h>

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


#define PRINT(x) printf(#x),\
   printf(" ("),\
   printf(TYPE_NAME(x)),\
   printf(") "),\
   printf(FORMATTER(x), x)

#define PRINT_ARRAY_ELEMENTS(x,n) ((void)_Generic((x),\
        double*: print_double_arr, \
        const double*: print_double_arr, \
        int*: print_int_arr )(x,n))

inline static void print_double_arr(const double *x, size_t n) {

    size_t n_nans = 0;
    size_t n_finite = 0;
    size_t n_positive = 0;
    size_t n_zero = 0;
    size_t n_negative = 0;
    size_t n_normal = 0;
    long double sum = 0;

    printf("[");
    for (size_t i=0; i<n; i++) {
        printf("%lf",x[i]);
        if (i!=n-1) {
            printf(", ");
        }
        if (isnan(x[i])) n_nans++;
        if (isfinite(x[i]) n_finite++;
        if (x[i] > 0) n_positive++;
        if (x[i] == 0) n_zero++;
        if (x[i] < 0) n_negative++;
        if (isnormal(x[i]) n_normal++;
    }
    printf("]\n");

    //todo: make description based on the counts or something
    //arrrghh this project got too big again, and I havent even implemented any arrays
}

inline static void print_int_arr(int *x, size_t n) {
    printf("is a int array");
}

#define PRINT_ARR(x,n) \
    PRINT(x),\
    printf("\n (type: "),\
    printf(TYPE_NAME(x[0])),\
    printf(") "),\
    PRINT_ARRAY_ELEMENTS(x,n)



