import sys

num_steps = int(sys.argv[1])

for step in range(1, num_steps + 1):
    print(" " * (num_steps - step), "#" * step, sep="")
