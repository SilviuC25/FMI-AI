# numbers between a and b that are divisible by their sum of digits
# 16 24

a = int(input("Enter number a: "))
b = int(input("Enter number b: "))

result = []

for num in range(a + 1, b):
    num_copy = num
    sum = 0
    while num_copy > 0:
        sum = sum + num_copy % 10
        num_copy = num_copy // 10
    if num % sum == 0:
        result.append(num)

print(', '.join(map(str, result)))