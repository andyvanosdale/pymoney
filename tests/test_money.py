import pytest
from money import Money


def test_init_nanos_under():
    with pytest.raises(ValueError):
        Money("USD", 0, -1_000_000_000)


def test_init_nanos_over():
    with pytest.raises(ValueError):
        Money("USD", 0, 1_000_000_000)


def test_init_neg_units_pos_nanos():
    with pytest.raises(ValueError):
        Money("USD", -1, 1)


def test_init_neg_units_zero_nanos():
    Money("USD", -1, 0)


def test_init_neg_units_neg_nanos():
    Money("USD", -1, -1)


def test_init_zero_units_zero_nanos():
    Money("USD", 0, 0)


def test_init_zero_units_pos_nanos():
    Money("USD", 0, 1)


def test_init_zero_units_neg_nanos():
    Money("USD", 0, -1)


def test_init_pos_units_zero_nanos():
    Money("USD", 1, 0)


def test_init_pos_units_pos_nanos():
    Money("USD", 1, 1)


def test_init_pos_units_neg_nanos():
    with pytest.raises(ValueError):
        Money("USD", 1, -1)


def test_eq_money():
    assert Money("USD", 10, 0) == Money("USD", 10, 0)


def test_eq_diff_currencycode():
    assert Money("USD", 10, 0) != Money("CAD", 10, 0)


def test_eq_int():
    assert Money("USD", 10, 0) != 10


def test_eq_float():
    assert Money("USD", 10, 0) != 10.0


def test_add_diff_currencycode():
    with pytest.raises(ValueError):
        _ = Money("USD", 10, 0) + Money("CAD", 10, 0)


def test_add_money():
    assert Money("USD", 0, 0) + Money("USD", 0, 0) == Money("USD", 0, 0)


def test_add_units():
    assert Money("USD", 10, 0) + Money("USD", 10, 0) == Money("USD", 20, 0)


def test_add_nanos():
    print(Money("USD", 0, 999_999_998) + Money("USD", 0, 1))
    assert Money("USD", 0, 999_999_998) + Money("USD", 0, 1) == Money(
        "USD", 0, 999_999_999
    )


def test_add_nanos_overflow():
    assert Money("USD", 0, 999_999_999) + Money("USD", 0, 1) == Money("USD", 1, 0)


def test_radd():
    # sending through sum will call radd behind the scenes with a default 0 (units)
    assert sum([Money("USD", 10, 0)]) == Money("USD", 10, 0)


def test_div_diff_currencycode():
    with pytest.raises(ValueError):
        _ = Money("USD", 10, 0) / Money("CAD", 10, 0)


def test_div_int():
    assert Money("USD", 10, 0) / 10 == Money("USD", 1, 0)


def test_div_units():
    assert Money("USD", 10, 0) / Money("USD", 10, 0) == Money("USD", 1, 0)


def test_div_nanos():
    assert Money("USD", 0, 50) / Money("USD", 0, 2) == Money("USD", 0, 25)


# TODO add more division tests
# TODO add subtraction tests
