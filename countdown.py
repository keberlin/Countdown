import argparse

from utils import elems, indexes

ADDITION = "+"
SUBTRACTION = "-"
MULTIPLICATION = "*"
DIVISION = "/"


def oper_level(operator):
    if operator in [ADDITION, SUBTRACTION]:
        return 0
    return 1


def bracket(operand, other):
    if other[2] is None or oper_level(operand[4]) == oper_level(other[4]):
        return format(other)
    return "(" + format(other) + ")"


def format(operand):
    if operand[2] is None:
        return str(operand[0])
    return f"{bracket(operand,operand[2])} {operand[4]} {bracket(operand,operand[3])}"


def oper(a, b):
    # Perform an addition between the 2 numbers
    yield (
        a[0] + b[0],
        a[1] + b[1],
        a,
        b,
        ADDITION,
    )
    # Perform a subtraction between the 2 numbers
    if a[0] > b[0]:
        yield (
            a[0] - b[0],
            a[1] + b[1],
            a,
            b,
            SUBTRACTION,
        )
    # In both directions
    if b[0] > a[0]:
        yield (
            b[0] - a[0],
            b[1] + a[1],
            b,
            a,
            SUBTRACTION,
        )
    # Perform a multiplication between the 2 numbers
    yield (
        a[0] * b[0],
        a[1] + b[1],
        a,
        b,
        MULTIPLICATION,
    )
    # Perform a division between the 2 numbers
    if b[0] and a[0] % b[0] == 0:
        yield (
            a[0] // b[0],
            a[1] + b[1],
            a,
            b,
            DIVISION,
        )
    # In both directions
    if a[0] and b[0] % a[0] == 0:
        yield (
            b[0] // a[0],
            b[1] + a[1],
            b,
            a,
            DIVISION,
        )


def perm(numbers):
    for n in numbers:
        yield (n, 1, None, None, None)

    array = list(range(len(numbers)))
    for n in range(len(numbers) // 2):
        for idx1, idx2 in indexes(array, n + 1):
            for a in perm(elems(numbers, idx1)):
                for b in perm(elems(numbers, idx2)):
                    for p in oper(a, b):
                        yield p


parser = argparse.ArgumentParser(description="Utility to solve the Countdown numbers game.")
parser.add_argument(dest="numbers", type=int, nargs=6, help="Numbers")
parser.add_argument(dest="total", type=int, nargs=1, help="Total")
args = parser.parse_args()

# 6 numbers results in 8,286,173 permutations

numbers = args.numbers
total = args.total[0]

results = list(filter(lambda x: x[0] == total, perm(numbers)))

# Sort in order of how many numbers were used
results.sort(key=lambda x: x[1])

if results:
    print(format(results[0]))
else:
    print("No exact solutions found.")
