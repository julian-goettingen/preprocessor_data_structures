// this can sort-of print anything and doesnt need much compiler-wise,
// but if there is an alternative we should use that alternative


#define PRINT(x) fprint_wild(stderr,#x, &x, sizeof(x))

void fprint_wild(FILE *f, const char* name, const void *p, size_t size);
void fprint_wild(FILE *f, const char* name, const void *p, size_t size) {
    // these cant be null if the function is called through the macro PRINT
    assert(p); 
    assert(name);
    fprintf(f,"(%s [hex dump of %ld bytes]::", name, size);
    const unsigned char *c = (const unsigned char *) p;
    for (size_t i=0; i<size; i++){
        fprintf(f, " %02x", c[i]);
    }
    fprintf(f,")\n");
}


#define PRINT_ARR(p,n) fprint_wild_array(stderr, #p, p, n, p==NULL?-1:sizeof(p[0]))

void fprint_wild_array(FILE *f, const char* name, const void *p, size_t n_elem, size_t element_size);
void fprint_wild_array(FILE *f, const char* name, const void *p, size_t n_elem, size_t element_size) {

    assert(name); // cant be null if called through the macro
    if (p==NULL) {
        fprintf(f,"(%s is NULL, but expected to hold %zu elements)", name, n_elem);
        return;
    }

    const char* c = (const char*)p;
    fprintf(f,"(%s [hex dump of %zu elements of size %zu bytes]::", name,n_elem, element_size);

    int show_all = 1;
    if (n_elem*element_size > 256) {
        show_all = 0;
    }
    else if (n_elem > 20) {
        show_all = 0;
    }
    else if (element_size > 8){
        show_all = 0;
    }

    if (show_all) {
        for (size_t i=0; i<n_elem; i++){
            fprintf(f,"(");
            for (size_t j=0; j<element_size; j++){
                fprintf(f, "%02x", c[i]);
            } 
            fprintf(f,")");
        }

    }
    else {
        // TODO: look for more bit-patterns that look suspiciously undefined?
        unsigned n_show = element_size<=8? 6: 3; // show first and last n_show elements
        int all_zeroes = 1;
        int all_ones = 1;

        for (size_t i=0; i<n_elem; i++){
            if (i<n_show || n_elem-i-1<n_show){
                fprintf(f,"(");
                for (size_t j=0; j<element_size; j++){
                    fprintf(f, "%02x", c[i]);
                } 
                fprintf(f,")");

                // we still loop the whole array which will often be useless but I dont care right now
                all_zeroes &= (c[i]==0);
                all_ones &= (c[i]==(char)0xFF);
            }
            if (i==n_show){
                fprintf(f," ... ");
            }
        }

        if (all_zeroes) {
            printf("entire memory is zeroed out\n");
        }
        if (all_ones) {
            printf("all bits are set to one\n");
        }
    }
    fprintf(f,")\n");
}

