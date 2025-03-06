import math


def is_prime(x: int)-> bool:
    """
    Check if number is a prime number.

    Parameters
    ----------
    x : int
        The number to check.

    Returns
    -------
    bool
        True if x is a prime number and False if not. 
    """    
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
