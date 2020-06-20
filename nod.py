a = 8
b = 2
while a != 0 and b != 0:
    if a > b:
        a = a % b
    else:
        b = b % b
c = a + b
print(c)