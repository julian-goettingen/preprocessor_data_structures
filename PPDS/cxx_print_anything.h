#include <cxxabi.h>
#include <iostream>
#include <assert.h>

#define PRINT(x) (std::cerr << "(" << abi::__cxa_demangle(typeid(x).name(),NULL,NULL,NULL) << " " << #x << " = " << (x) << ")" << std::endl)

#define PRINT_ARR(x,n) (PRINT(x), std::cerr << " is an array of size ", PRINT(n), print_elements(x,n))


template<typename T, typename N>
static void print_elements(T x,N n) {

    typeof(n) cutoff = 20;
    typeof(n) n_show = 6;
    assert(n_show*2 <= cutoff);

    std::cerr << n << " elements: (";

    if (n <= cutoff)
        for (typeof(n) i=0; i<n; i++) {
            std::cerr << x[i];
            if (i!=n-1) {
                std::cerr << ", ";
            }
        }
    else {
        for (typeof(n) i=0; i<n_show; i++) {
            std::cerr << x[i] << ", ";
        }
        std::cerr << " ... ";
        for (typeof(n) i=n-n_show-1; i<n; i++) {
            std::cerr << x[i];
            if (i!=n-1) {
                std::cerr << ", ";
            }    
        }
    }
    std::cerr << ")\n";
}

