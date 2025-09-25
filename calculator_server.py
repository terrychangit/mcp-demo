from mcp.server.fastmcp import FastMCP
import logging
import math
from typing import Union, NoReturn, Any

# Configure logging with better formatting and file output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculator_server.log'),
        logging.StreamHandler()
    ]
)
logger: logging.Logger = logging.getLogger(__name__)

mcp: FastMCP = FastMCP("Calculator MCP Server")

# Security constants
MAX_INPUT_VALUE: float = 1e308  # Near float max to prevent overflow
MIN_INPUT_VALUE: float = -1e308
MAX_PRECISION: int = 15  # Maximum decimal places to prevent precision issues

def validate_number(value: Union[int, float], param_name: str) -> Union[int, float]:
    """Enhanced validation for numeric inputs with security checks.

    Args:
        value: The value to validate
        param_name: Name of the parameter for error messages

    Returns:
        The validated number

    Raises:
        ValueError: If validation fails
    """
    # Type check
    if not isinstance(value, (int, float)):
        raise ValueError(f"Parameter '{param_name}' must be a number (int or float), "
                        f"but received {type(value).__name__}: {value}")

    # Check for NaN or Infinity
    if math.isnan(value):
        raise ValueError(f"Parameter '{param_name}' cannot be NaN (Not a Number)")
    if math.isinf(value):
        raise ValueError(f"Parameter '{param_name}' cannot be infinity")

    # Size limits to prevent overflow/underflow issues
    if not (MIN_INPUT_VALUE <= value <= MAX_INPUT_VALUE):
        raise ValueError(f"Parameter '{param_name}' value {value} is outside the allowed range "
                        f"[{MIN_INPUT_VALUE}, {MAX_INPUT_VALUE}]")

    return value

@mcp.tool()
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers
    """
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        result = a + b
        logger.info(f"add({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in add: {e}")
        raise

@mcp.tool()
def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of the two numbers
    """
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        result = a * b
        logger.info(f"multiply({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in multiply: {e}")
        raise

@mcp.tool()
def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Subtract second number from first number.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference of the two numbers
    """
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        result = a - b
        logger.info(f"subtract({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in subtract: {e}")
        raise

@mcp.tool()
def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Divide first number by second number.

    Args:
        a: Dividend (number to be divided)
        b: Divisor (number to divide by, cannot be zero)

    Returns:
        Quotient of the division

    Raises:
        ValueError: If divisor is zero or inputs are invalid
    """
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")

        # Check for division by zero with more descriptive message
        if b == 0:
            raise ValueError("Division by zero is not allowed. The divisor (b) cannot be zero.")

        result = a / b

        # Check for potential overflow in result
        if not (MIN_INPUT_VALUE <= result <= MAX_INPUT_VALUE):
            raise ValueError(f"Division result {result} is outside the valid range. "
                           f"Consider using smaller input values.")

        logger.info(f"divide({a}, {b}) = {result}")
        return result
    except ValueError as e:
        logger.error(f"Validation error in divide: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in divide: {e}")
        raise ValueError(f"Failed to perform division: {str(e)}")

@mcp.tool()
def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Raise base to the power of exponent.

    Args:
        base: Base number
        exponent: Exponent (power to raise base to)

    Returns:
        Base raised to the power of exponent

    Raises:
        ValueError: If result would be invalid (overflow, undefined, etc.)
        OverflowError: If result is too large to represent
    """
    try:
        base = validate_number(base, "base")
        exponent = validate_number(exponent, "exponent")

        # Check for potential issues with 0^0
        if base == 0 and exponent == 0:
            raise ValueError("0^0 is mathematically undefined. Please use non-zero base or exponent.")

        # Check for very large exponents that could cause overflow
        if abs(exponent) > 1000:
            raise ValueError(f"Exponent {exponent} is too large. Maximum allowed is 1000.")

        result = base ** exponent

        # Check if result is valid
        if math.isnan(result):
            raise ValueError(f"Power operation resulted in NaN. This may occur with negative base and non-integer exponent.")
        if math.isinf(result):
            raise ValueError(f"Power operation resulted in infinity. Result is too large to represent.")

        # Additional check for overflow
        if not (MIN_INPUT_VALUE <= result <= MAX_INPUT_VALUE):
            raise OverflowError(f"Power result {result} exceeds representable range.")

        logger.info(f"power({base}, {exponent}) = {result}")
        return result
    except (ValueError, OverflowError) as e:
        logger.error(f"Validation error in power: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in power: {e}")
        raise ValueError(f"Failed to perform power operation: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting Calculator MCP Server")
    mcp.run(transport="stdio")  # Use STDIO for local subprocess communication