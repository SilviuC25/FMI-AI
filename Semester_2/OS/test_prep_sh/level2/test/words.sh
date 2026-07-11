#!/bin/bash

words=""

while true; do
	read word
	if [ "$word" = "stop" ]; then
		break
	fi
	words="$words $word"
done

echo "$words"
