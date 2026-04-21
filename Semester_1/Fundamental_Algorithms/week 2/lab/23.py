# common digits of x and y
# 21348 14153

x = int(input("Enter number x: "))
y = int(input("Enter number y: "))

is_digit_of_x = {}
is_digit_of_y = {}

while x > 0:
    is_digit_of_x[x % 10] = True
    x = x // 10

while y > 0:
    is_digit_of_y[y % 10] = True
    y = y // 10

result = []

for digit in range(0, 10):
    if is_digit_of_x.get(digit) and is_digit_of_y.get(digit):
        result.append(digit)

print(len(result))
print("Digits: ")
print(', '.join(map(str, result)))