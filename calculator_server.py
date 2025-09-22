from mcp.server.fastmcp import FastMCP
import logging
from typing import Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("Calculator MCP Server")

def validate_number(value: Union[int, float], param_name: str) -> Union[int, float]:
    """Validate that the input is a number."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{param_name} must be a number, got {type(value).__name__}")
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
        a: Dividend
        b: Divisor (must not be zero)

    Returns:
        Quotient of the division
    """
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        result = a / b
        logger.info(f"divide({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in divide: {e}")
        raise

@mcp.tool()
def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Raise base to the power of exponent.

    Args:
        base: Base number
        exponent: Exponent

    Returns:
        Base raised to the power of exponent
    """
    try:
        base = validate_number(base, "base")
        exponent = validate_number(exponent, "exponent")
        result = base ** exponent
        logger.info(f"power({base}, {exponent}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in power: {e}")
        raise

if __name__ == "__main__":
    logger.info("Starting Calculator MCP Server")
    mcp.run(transport="stdio")  # Use STDIO for local subprocess communication