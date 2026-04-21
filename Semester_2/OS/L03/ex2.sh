#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Correct Syntax: $0 file1 file2"
	exit 1
fi

file1=$1
file2=$2
count=0

exec 3< "$file1"
exec 4< "$file2"

while read -u3 line1 && read -u4 line2; do
	if [ "$line1" != "$line2" ]; then
		((count++))

		echo "Diff $count found:"
		echo "   File1: $line1"
		echo "   File2: $line2"
	fi

	if [ $count -eq 3 ]; then
		break
	fi
done

exec 3<&-
exec 4<&-

