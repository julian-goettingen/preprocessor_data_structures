#define _POSIX_C_SOURCE 2
#include "send2py.h"
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>


#define ERR_EXIT(msg) do{fprintf(stderr, msg); return -1;}while(0)
#define FIN_MSG "FINISH;"

FILE *process = NULL;
int pfd = 0;


int init_pipe() {

    if (process) ERR_EXIT("init was already called");
    process = popen("python3 run_server.py", "w");
    if (!process) ERR_EXIT("popen failed");

    pfd = fileno(process);
    if (pfd == -1) ERR_EXIT("getting fileno failed");

    fprintf(stderr, "opened the pipe");
    return 0;
}

int close_pipe() {
    if (!process) ERR_EXIT("pipe was closed twice or closed before being opened");
    str_to_py(FIN_MSG, strlen(FIN_MSG));
    fprintf(stderr, "closing the pipe...\n");
    int err = pclose(process);
    fprintf(stderr, "closed the pipe, exit status %d\n", err);
    return err;
}


int str_to_py(const char *x, size_t n) {

    fprintf(stderr, "in str_to_py\n");

    size_t i = 0;
    do {
        ssize_t written = write(pfd, x+i, n-i);
        if (written < 0) ERR_EXIT("write failed");
        fprintf(stderr, "wrote %zu bytes\n", written);
        i += written;
    } while (i<n);
    return 0;
}