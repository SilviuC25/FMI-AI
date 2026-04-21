#1) a)
print("1) a)\n")
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))
sum = a + b
print(f"Sum of {a} and {b} is {sum}")

#1) b)
print("1) b)\n")
n = int(input("Enter the number: "))
product = 1
for i in range (2, n + 1):
    product = product * i
print(f"The product is {product}")

#1) c)
print("1) c)\n")
n = int(input("Enter the number: "))
zeros = 0
for i in range(5, n + 1, 5):
    c = i
    while c % 5 == 0:
        c = c // 5
        zeros = zeros + 1
    
print(f"The number of {zeros}")

#1) d)
print("1) d)\n")
n = int(input("Enter the number: "))
sum = 0
for i in range(1, n + 1):
    if n % i == 0:
        sum = sum + i

if sum <= n:
    print(f"n is a perfect number")
else:
    print(f"n is not a perfect number")
