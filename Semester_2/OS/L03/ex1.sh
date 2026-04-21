#!/bin/bash
if [ $# -ne 2 ]; then
	echo "Correct Syntax: $0 number1 number2"
	exit 1
fi

number1=$1
number2=$2

sum=$((number1 + number2))
diff=$((number1 - number2))
product=$((number1 * number2))

echo "The sum is equal to: $sum"
echo "The difference is equal to: $diff"
echo "The product is equal to: $product"

