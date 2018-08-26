import sys

n, w = map(int, sys.stdin.readline().split())

CUTENESS = [0] * (n + 1)
FATNESS = [0] * (n + 1)
MostCute = [0] * (n + 1)
catgirls = 1

for i in range(n):
    event = sys.stdin.readline().rstrip().split()
    if event[0] == 'A':
        FATNESS[catgirls] = int(event[1]) + FATNESS[catgirls - 1]
        CUTENESS[catgirls] = int(event[2]) + CUTENESS[catgirls - 1]
        low = 0
        high = catgirls
        while low <= high:
            middle = low + (high - low) / 2
            if FATNESS[catgirls] - FATNESS[middle] <= w:
                high = middle - 1
            else:
                low = middle + 1
        MostCute[catgirls] = max(MostCute[catgirls - 1], CUTENESS[catgirls] - CUTENESS[low])
        print MostCute[catgirls]
        catgirls += 1
    else:
        catgirls -= 1
