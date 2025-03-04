import math


def is_prime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False

    for y in range(3, int(math.sqrt(x)) + 1, 2):
        if x % y == 0:
            return False
    return True
