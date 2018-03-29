import sys

if len(sys.argv) > 1:
    n = int(sys.argv[1])
    print('{}{}' . format((n // 60) % 24, n % 60))
else:
    print(sys.argv)
