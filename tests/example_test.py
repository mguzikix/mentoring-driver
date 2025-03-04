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
def test_is_prime(input_n, expected):
    assert is_prime(input_n) == expected
