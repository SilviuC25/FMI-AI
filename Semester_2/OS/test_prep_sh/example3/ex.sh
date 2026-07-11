#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Use a source file as the parameter"
	exit 1
fi

C_FILE=$1

if [ ! -f "$C_FILE" ]; then
	echo "The file '$C_FILE' does not exist"
	exit 1
fi

FUNCTIONS=$(grep -E '^[a-zA-Z_][a-zA-Z0-9_*]+\s+[a-zA-Z_][a-zA-Z0-9_*]*\s*(' "$C_FILE" | sed -E 's/.*[ *]'
