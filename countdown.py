import argparse


def oper(a, b):
    # Perform an addition between the 2 numbers
    yield a[0] + b[0], f"({a[1]}+{b[1]})"
    # Perform a subtraction between the 2 numbers
    if a[0] > b[0]:
        yield a[0] - b[0], f"({a[1]}-{b[1]})"
    # In both directions
    if b[0] > a[0]:
        yield b[0] - a[0], f"({b[1]}-{a[1]})"
    # Perform a multiplication between the 2 numbers
    yield a[0] * b[0], f"({a[1]}*{b[1]})"
    # Perform a division between the 2 numbers
    if b[0] and a[0] % b[0] == 0:
        yield a[0] // b[0], f"({a[1]}/{b[1]})"
    # In both directions
    if a[0] and b[0] % a[0] == 0:
        yield b[0] // a[0], f"({b[1]}/{a[1]})"


def inverse(idx, sub):
    return list(set(idx) - set(sub))


def indexes(idx, n):
    for i in idx:
        idx1 = [i]
        if n > 1:
            for idx2, idx3 in indexes(inverse(idx, idx1), n - 1):
                yield idx1 + idx2, idx3
        else:
            yield idx1, inverse(idx, idx1)


def elems(numbers, idx):
    return [numbers[i] for i in idx]


def perm(numbers):
    for n in numbers:
        yield n, str(n)

    for n in range(len(numbers) // 2):
        for idx1, idx2 in indexes(range(len(numbers)), n + 1):
            for a in perm(elems(numbers, idx1)):
                for b in perm(elems(numbers, idx2)):
                    for x, y in oper(a, b):
                        yield x, y


parser = argparse.ArgumentParser(
    description="Utility to solve the Countdown numbers games."
)
parser.add_argument(dest="numbers", type=int, nargs=6, help="Numbers")
parser.add_argument(dest="total", type=int, nargs=1, help="Total")
args = parser.parse_args()

# 6 numbers results in 8286173 permutations

numbers = args.numbers
total = args.total[0]

results = []
for v in perm(numbers):
    if v[0] == total:
        results.append(v[1])

# Remove duplicates
results = list(set(results))

results.sort(key=lambda x: len(x))

for result in results:
    print(result)
