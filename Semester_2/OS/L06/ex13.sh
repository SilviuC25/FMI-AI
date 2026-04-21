#!/bin/bash

source_file=$1
output_dir="dictionaries"

mkdir -p $output_dir

for digit in {0..9}; do
	grep "^$digit" $source_file | sort > "$output_dir/file_$digit.txt"
done
