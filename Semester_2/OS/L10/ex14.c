#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        return 1;
    }

    int parentToChildPipe[2];
    int childToParentPipe[2];

    if (pipe(parentToChildPipe) == -1 || pipe(childToParentPipe) == -1) {
        return 1;
    }

    pid_t pid = fork();

    if (pid < 0) {
        return 1;
    }

    if (pid == 0) {
        close(parentToChildPipe[1]);
        close(childToParentPipe[0]);

        char filename[256];
        ssize_t bytesRead = read(parentToChildPipe[0], filename, sizeof(filename) - 1);
        
        if (bytesRead > 0) {
            filename[bytesRead] = '\0';
            
            int fileDescriptor = open(filename, O_RDONLY);
            if (fileDescriptor == -1) {
                char *errorMsg = "Error: File not found.";
                write(childToParentPipe[1], errorMsg, strlen(errorMsg));
            } else {
                char buffer[1024];
                ssize_t n;
                while ((n = read(fileDescriptor, buffer, sizeof(buffer))) > 0) {
                    write(childToParentPipe[1], buffer, n);
                }
                close(fileDescriptor);
            }
        }

        close(parentToChildPipe[0]);
        close(childToParentPipe[1]);
        exit(0);
    } else {
        close(parentToChildPipe[0]);
        close(childToParentPipe[1]);

        write(parentToChildPipe[1], argv[1], strlen(argv[1]));
        close(parentToChildPipe[1]);

        char responseBuffer[1024];
        ssize_t n;
        while ((n = read(childToParentPipe[0], responseBuffer, sizeof(responseBuffer))) > 0) {
            write(STDOUT_FILENO, responseBuffer, n);
        }
        printf("\n");

        close(childToParentPipe[0]);
        wait(NULL);
    }

    return 0;
}
