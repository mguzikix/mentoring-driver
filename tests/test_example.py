import pytest
from driver_mguzikix.example import is_prime


@pytest.mark.parametrize(
    ("input_n", "expected"),
    (
        (1, False),
        (1, False),
        (2, True),
        (7, True),
        (75, False),
        (3877, True),
        (-11111, False)
    ),
)
def test_is_prime(input_n: int, expected: bool) -> None:
    """
    Test for is_prime function

    Parameters
    ----------
    input_n : int
        The number to be checked by is_prime function.
    expected : bool
        True if input_n is prime number and False if not. 
    """    
    assert is_prime(input_n) == expected
