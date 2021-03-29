import argparse

from utils import elems, indexes

ADDITION = "+"
SUBTRACTION = "-"
MULTIPLICATION = "*"
DIVISION = "/"


class Number:
    def __init__(self, number):
        self.total = number
        self.count = 1
        self.number = str(number)

    def __str__(self):
        return self.number


class Product:
    def __init__(
        self, total, count, left, right, operator,
    ):
        self.total = total
        self.count = count
        self.left = left
        self.right = right
        self.operator = operator

    def oper_level(self):
        if self.operator in [ADDITION, SUBTRACTION]:
            return 0
        return 1

    def bracket(self, p):
        if isinstance(p, Number) or self.oper_level() == p.oper_level():
            return str(p)
        return "(" + str(p) + ")"

    def __str__(self):
        return f"{self.bracket(self.left)} {self.operator} {self.bracket(self.right)}"


def oper(a, b):
    # Perform an addition between the 2 numbers
    yield Product(
        total=a.total + b.total,
        count=a.count + b.count,
        left=a,
        right=b,
        operator=ADDITION,
    )
    # Perform a subtraction between the 2 numbers
    if a.total > b.total:
        yield Product(
            total=a.total - b.total,
            count=a.count + b.count,
            left=a,
            right=b,
            operator=SUBTRACTION,
        )
    # In both directions
    if b.total > a.total:
        yield Product(
            total=b.total - a.total,
            count=a.count + b.count,
            left=b,
            right=a,
            operator=SUBTRACTION,
        )
    # Perform a multiplication between the 2 numbers
    yield Product(
        total=a.total * b.total,
        count=a.count + b.count,
        left=a,
        right=b,
        operator=MULTIPLICATION,
    )
    # Perform a division between the 2 numbers
    if b.total and a.total % b.total == 0:
        yield Product(
            total=a.total // b.total,
            count=a.count + b.count,
            left=a,
            right=b,
            operator=DIVISION,
        )
    # In both directions
    if a.total and b.total % a.total == 0:
        yield Product(
            total=b.total // a.total,
            count=a.count + b.count,
            left=b,
            right=a,
            operator=DIVISION,
        )


def perm(numbers):
    for n in numbers:
        yield Number(n)

    array = list(range(len(numbers)))
    for n in range(len(numbers) // 2):
        for idx1, idx2 in indexes(array, n + 1):
            for a in perm(elems(numbers, idx1)):
                for b in perm(elems(numbers, idx2)):
                    for p in oper(a, b):
                        yield p


parser = argparse.ArgumentParser(
    description="Utility to solve the Countdown numbers game."
)
parser.add_argument(dest="numbers", type=int, nargs=6, help="Numbers")
parser.add_argument(dest="total", type=int, nargs=1, help="Total")
args = parser.parse_args()

# 6 numbers results in 8,286,173 permutations

numbers = args.numbers
total = args.total[0]

results = list(filter(lambda x: x.total == total, perm(numbers)))

# Sort in order of how many numbers were used
results.sort(key=lambda x: x.count)

if results:
    print(results[0])
else:
    print("No exact solutions found.")
