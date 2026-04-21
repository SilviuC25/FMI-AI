#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>

int main(int argc, char *argv[]) {
	int in_file = open(argv[1], O_RDONLY);
	int out_file = open("out.bin", O_WRONLY | O_CREAT | O_TRUNC, 0644);

	bool even = true;
	char current_ch;

	while (read(in_file, &current_ch, 1)) {
		if (even) {
			write(out_file, &current_ch, 1);
		}
		write(out_file, &current_ch, 1);
		even = !even;
	}

	close(in_file);
	close(out_file);
	return 0;
}
