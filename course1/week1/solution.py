import sys
digit_string = sys.argv[1]
sum = 0
for num in digit_string:
    sum += int(num)
print(sum)