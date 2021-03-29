def indexes(idx, n):
    for i, x in enumerate(idx):
        idx1 = [x]
        idx1_inv = idx[:i] + idx[i + 1 :]
        if n > 1:
            for idx2, idx3 in indexes(idx1_inv, n - 1):
                yield idx1 + idx2, idx3
        else:
            yield idx1, idx1_inv


def elems(numbers, idx):
    return [numbers[i] for i in idx]
