from functools import wraps
from collections import defaultdict


solution = {}


def parse_solution(n):
    left_split, right_split = solution[n]
    if right_split == 0:
        return [left_split]
    return parse_solution(left_split) + parse_solution(right_split)


def memo(f):
    already_computed = {}

    @wraps(f)
    def _wrap(n):
        """
            Looking at whether function was already calculated
        """
        if already_computed.get(n):
            res = already_computed[n]
        else:
            res = f(n)
            already_computed[n] = res
        return res

    return _wrap


@memo
# @get_call_times
def r(n):
    """
    Args: n is the iron length
    return: the maximum revenue
    """

    max_price, max_split = max(
        [(price[n], 0)] + [(r(i) + r(n - i), i) for i in range(1, n)], key=lambda x: x[0]
    )
    solution[n] = (n - max_split, max_split)
    return max_price


if __name__ == '__main__':
    original_price = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 35]
    price = defaultdict(int)
    for index, value in enumerate(original_price):
        price[index + 1] = value
    r(20)
    print(parse_solution(20))
