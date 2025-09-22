# MCP Calculator Demo

A demonstration of the Model Context Protocol (MCP) with a calculator server and client that integrates with Azure OpenAI.

## Features

- **Calculator Server**: Provides mathematical operations as MCP tools
  - Addition (`add`)
  - Multiplication (`multiply`)
  - Subtraction (`subtract`)
  - Division (`divide`)
  - Power/Exponentiation (`power`)

- **Client**: Demonstrates MCP usage with two modes:
  - Basic: Direct tool invocation
  - AI-Integrated: Natural language queries processed by Azure OpenAI with tool calling

- **Error Handling**: Comprehensive validation and error handling
- **Logging**: Detailed logging for debugging and monitoring
- **Testing**: Unit tests for calculator functions

## Prerequisites

- Python 3.8+
- Azure OpenAI account (for AI-integrated demo)

## Installation

1. Clone or download this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade pip
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Azure OpenAI Configuration (optional, for AI demo)
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

The AI-integrated demo will be skipped if Azure OpenAI credentials are not configured.

## Usage

### Running the Demo

Execute the client to see both basic and AI-integrated demos:

```bash
python client.py
```

### Expected Output

1. **Basic Demo**: Lists available tools and demonstrates direct tool invocation
2. **AI-Integrated Demo**: Processes natural language queries using Azure OpenAI (if configured)

### Manual Server Usage

You can also run the server independently:

```bash
python calculator_server.py
```

The server uses STDIO transport for MCP communication.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `add` | Add two numbers | `a`: number, `b`: number |
| `multiply` | Multiply two numbers | `a`: number, `b`: number |
| `subtract` | Subtract second number from first | `a`: number, `b`: number |
| `divide` | Divide first number by second | `a`: number, `b`: number (non-zero) |
| `power` | Raise base to exponent | `base`: number, `exponent`: number |

## Testing

Run the test suite:

```bash
python -m pytest test_calculator_server.py -v
```

## Architecture

```
┌─────────────────┐    STDIO    ┌─────────────────┐
│   Client.py     │◄──────────►│ Calculator      │
│                 │             │ Server.py       │
│ - Basic Demo    │             │                 │
│ - AI Integration│             │ - Add Tool      │
│   (Azure OpenAI)│             │ - Multiply Tool │
└─────────────────┘             │ - Subtract Tool │
                                │ - Divide Tool   │
                                │ - Power Tool    │
                                └─────────────────┘
```

## Error Handling

- Input validation for all calculator operations
- Division by zero prevention
- Azure OpenAI credential validation
- Comprehensive logging for troubleshooting

## Development

### Adding New Tools

1. Define the tool function in `calculator_server.py`
2. Decorate with `@mcp.tool()`
3. Add input validation and error handling
4. Include logging
5. Update the tool list in `client.py` print statements
6. Add corresponding tests in `test_calculator_server.py`

### Code Structure

- `calculator_server.py`: MCP server with calculator tools
- `client.py`: MCP client with demo implementations
- `test_calculator_server.py`: Unit tests
- `requirements.txt`: Python dependencies
- `.gitignore`: Git ignore patterns

## License

This project is for demonstration purposes. Feel free to modify and extend.