for user in "$@"; do
	if who | grep -q -w "^$user"; then
		echo -e "User $user is connected\n"
	else
		echo -e "User $user is not connected\n"
	fi
done
