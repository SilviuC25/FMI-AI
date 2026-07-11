#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Error: 2 parameters needed to compute the sum"
	exit 1
fi

a=$1
b=$2

sum=$(( $a + $b ))

echo $sum
