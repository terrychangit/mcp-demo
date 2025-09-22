import pytest
from calculator_server import add, multiply, subtract, divide, power, validate_number

class TestValidateNumber:
    def test_valid_int(self):
        assert validate_number(5, "test") == 5

    def test_valid_float(self):
        assert validate_number(3.14, "test") == 3.14

    def test_invalid_string(self):
        with pytest.raises(ValueError, match="test must be a number"):
            validate_number("not_a_number", "test")

    def test_invalid_list(self):
        with pytest.raises(ValueError, match="test must be a number"):
            validate_number([1, 2, 3], "test")

class TestAdd:
    def test_add_integers(self):
        assert add(2, 3) == 5

    def test_add_floats(self):
        assert add(2.5, 3.7) == 6.2

    def test_add_mixed(self):
        assert add(2, 3.5) == 5.5

    def test_add_negative(self):
        assert add(-2, 3) == 1

    def test_add_invalid_input(self):
        with pytest.raises(ValueError):
            add("a", 3)

class TestMultiply:
    def test_multiply_integers(self):
        assert multiply(2, 3) == 6

    def test_multiply_floats(self):
        assert multiply(2.5, 4.0) == 10.0

    def test_multiply_zero(self):
        assert multiply(0, 5) == 0

    def test_multiply_negative(self):
        assert multiply(-2, 3) == -6

class TestSubtract:
    def test_subtract_integers(self):
        assert subtract(5, 3) == 2

    def test_subtract_floats(self):
        assert subtract(5.5, 2.2) == 3.3

    def test_subtract_negative_result(self):
        assert subtract(3, 5) == -2

class TestDivide:
    def test_divide_integers(self):
        assert divide(6, 2) == 3

    def test_divide_floats(self):
        assert divide(5.0, 2.0) == 2.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            divide(5, 0)

    def test_divide_negative(self):
        assert divide(-6, 2) == -3

class TestPower:
    def test_power_integers(self):
        assert power(2, 3) == 8

    def test_power_float_base(self):
        assert power(2.0, 3) == 8.0

    def test_power_zero_exponent(self):
        assert power(5, 0) == 1

    def test_power_negative_exponent(self):
        assert power(2, -1) == 0.5

    def test_power_fractional_exponent(self):
        assert power(4, 0.5) == 2.0

if __name__ == "__main__":
    pytest.main([__file__])