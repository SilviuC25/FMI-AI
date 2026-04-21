#!/bin/bash

for file in "$@"; do
	if [ -f "$file" ]; then
		awk '
		length($0) > 10 {
			count++
			print "Line " NR ": " substr($0, 11)
		}
		END {
			print "File: " FILENAME
			print "Lines printed: " count + 0
		}
		' "$file"

		echo -e "\n"
	else 
		echo -e "Invalid file: $file"
	fi
done
