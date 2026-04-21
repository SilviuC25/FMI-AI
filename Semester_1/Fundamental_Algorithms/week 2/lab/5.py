# smallest number that can be formed
# 45001

num = int(input("Enter the number: "))
digits = []

while num > 0:
    digits.append(num % 10)
    num = num // 10

digits.sort()

for digit in digits:
    if digit % 10 != 0:
        print(digit, end='')
        break

first_digit = False

for digit in digits:
    if digit % 10 != 0 and first_digit == True:
        print(digit, end='')
    elif digit % 10 == 0:
        print(digit, end='')
    else:
        first_digit = True