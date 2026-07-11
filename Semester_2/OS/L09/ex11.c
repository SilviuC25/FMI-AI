#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        return 1;
    }

    int x = atoi(argv[1]);
    int n = argc - 3;
    int r = atoi(argv[argc - 1]);

    for (int i = n + 1; i >= 2; i--) {
        int status;
        pid_t pid = fork();

        if (pid < 0) {
            return 1;
        }

        if (pid == 0) {
            int ai = atoi(argv[i]);
            r = (r * x) + ai;
            exit(r);
        } else {
            wait(&status);
            if (WIFEXITED(status)) {
                r = WEXITSTATUS(status);
            }
        }
    }

    printf("%d\n", r);

    return 0;
}
