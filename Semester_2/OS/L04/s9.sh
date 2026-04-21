#!/bin/bash

for file in "$@"; do
	if [ -f "$file" ]; then
		echo -e "File $file:"
		sed -E 's/^([a-zA-Z0-9]+ )([a-zA-Z0-9]+ )([a-zA-Z0-9]+ )([a-zA-Z0-9]+ )/\1\3/' "$file"
		echo -e "\n"
	else
		echo "Invalid file: $file"
	fi
done

