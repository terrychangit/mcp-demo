from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator MCP Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")  # Use STDIO for local subprocess communication