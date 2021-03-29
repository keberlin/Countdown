from utils import elems, indexes


def test_indexes():
    array = list(range(3))
    results = list(indexes(array, 1))
    assert results == [([0], [1, 2]), ([1], [0, 2]), ([2], [0, 1])]

    array = list(range(3))
    results = list(indexes(array, 2))
    assert results == [
        ([0, 1], [2]),
        ([0, 2], [1]),
        ([1, 0], [2]),
        ([1, 2], [0]),
        ([2, 0], [1]),
        ([2, 1], [0]),
    ]


def test_elems():
    array = ["A", "B", "C", "D", "E", "F"]
    results = elems(array, [1, 2, 3])
    assert results == ["B", "C", "D"]
