import argparse

ADDITION = "+"
SUBTRACTION = "-"
MULTIPLICATION = "*"
DIVISION = "/"


def oper_level(o):
    if o == ADDITION or o == SUBTRACTION:
        return 0
    return 1


class Perm:
    def __init__(
        self, total, count, number=None, left=None, right=None, operator=None,
    ):
        self.total = total
        self.count = count
        self.number = number
        self.left = left
        self.right = right
        self.operator = operator

    def bracket(self, p):
        if p.number or oper_level(self.operator) == oper_level(p.operator):
            return str(p)
        return "(" + str(p) + ")"

    def __str__(self):
        if self.number:
            return self.number
        return f"{self.bracket(self.left)} {self.operator} {self.bracket(self.right)}"


def oper(a, b):
    # Perform an addition between the 2 numbers
    yield Perm(
        total=a.total + b.total,
        count=a.count + b.count,
        left=a,
        right=b,
        operator=ADDITION,
    )
    # Perform a subtraction between the 2 numbers
    if a.total > b.total:
        yield Perm(
            total=a.total - b.total,
            count=a.count + b.count,
            left=a,
            right=b,
            operator=SUBTRACTION,
        )
    # In both directions
    if b.total > a.total:
        yield Perm(
            total=b.total - a.total,
            count=a.count + b.count,
            left=b,
            right=a,
            operator=SUBTRACTION,
        )
    # Perform a multiplication between the 2 numbers
    yield Perm(
        total=a.total * b.total,
        count=a.count + b.count,
        left=a,
        right=b,
        operator=MULTIPLICATION,
    )
    # Perform a division between the 2 numbers
    if b.total and a.total % b.total == 0:
        yield Perm(
            total=a.total // b.total,
            count=a.count + b.count,
            left=a,
            right=b,
            operator=DIVISION,
        )
    # In both directions
    if a.total and b.total % a.total == 0:
        yield Perm(
            total=b.total // a.total,
            count=a.count + b.count,
            left=b,
            right=a,
            operator=DIVISION,
        )


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
        yield Perm(total=n, count=1, number=str(n))

    for n in range(len(numbers) // 2):
        for idx1, idx2 in indexes(range(len(numbers)), n + 1):
            for a in perm(elems(numbers, idx1)):
                for b in perm(elems(numbers, idx2)):
                    for p in oper(a, b):
                        yield p


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
for p in perm(numbers):
    if p.total == total:
        results.append(p)

# Remove duplicates
# results = list(set(results))

# Sort in order of how many numbers were used
results.sort(key=lambda x: x.count)

for result in results:
    print(result)
