# numbers with sum of the digits divisible by k
# 26 4

n = int(input("Enter number n: "))
k = int(input("Enter number k: "))

result = []

for number in range(10, n):
    number_copy = number
    sum = 0
    while number_copy:
        sum = sum + number_copy % 10
        number_copy = number_copy // 10
    if sum % k == 0:
        result.append(number)

print(', '.join(map(str, result)))
