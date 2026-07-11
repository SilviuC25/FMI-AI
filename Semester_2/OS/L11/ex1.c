#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    const char *fifoDigitsPath = "fifo_digits";
    const char *fifoLettersPath = "fifo_letters";

    mkfifo(fifoDigitsPath, 0666);
    mkfifo(fifoLettersPath, 0666);

    pid_t pidChild2 = fork();
    if (pidChild2 < 0) {
        return 1;
    }

    if (pidChild2 == 0) {
        int fdDigits = open(fifoDigitsPath, O_RDONLY);
        if (fdDigits == -1) {
            exit(1);
        }

        char buffer[1024];
        ssize_t bytesRead;

        while ((bytesRead = read(fdDigits, buffer, sizeof(buffer))) > 0) {
            write(STDOUT_FILENO, buffer, bytesRead);
        }

        close(fdDigits);
        exit(0);
    }

    pid_t pidChild3 = fork();
    if (pidChild3 < 0) {
        return 1;
    }

    if (pidChild3 == 0) {
        int fdLetters = open(fifoLettersPath, O_RDONLY);
        if (fdLetters == -1) {
            exit(1);
        }

        char buffer[1024];
        ssize_t bytesRead;

        while ((bytesRead = read(fdLetters, buffer, sizeof(buffer))) > 0) {
            for (ssize_t i = 0; i < bytesRead; i++) {
                buffer[i] = toupper((unsigned char)buffer[i]);
            }
            write(STDOUT_FILENO, buffer, bytesRead);
        }

        close(fdLetters);
        exit(0);
    }

    int fdDigitsWrite = open(fifoDigitsPath, O_WRONLY);
    int fdLettersWrite = open(fifoLettersPath, O_WRONLY);

    char inputLine[32];
    while (fgets(inputLine, sizeof(inputLine), stdin) != NULL) {
        size_t length = strlen(inputLine);
        
        for (size_t i = 0; i < length; i++) {
            if (isdigit((unsigned char)inputLine[i])) {
                write(fdDigitsWrite, &inputLine[i], 1);
            } else if (isalpha((unsigned char)inputLine[i])) {
                write(fdLettersWrite, &inputLine[i], 1);
            }
        }

        write(fdDigitsWrite, "\n", 1);
        write(fdLettersWrite, "\n", 1);
    }

    close(fdDigitsWrite);
    close(fdLettersWrite);

    wait(NULL);
    wait(NULL);

   
    return 0;
}
