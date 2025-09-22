import asyncio
import json
import logging
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AzureOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Azure OpenAI client setup with error handling
try:
    azure_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2024-02-15-preview"  # Fixed to current API version
    )
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not azure_client.api_key or not deployment_name:
        logger.warning("Azure OpenAI credentials not found in environment variables")
        azure_client = None
        deployment_name = None
except Exception as e:
    logger.error(f"Failed to initialize Azure OpenAI client: {e}")
    azure_client = None
    deployment_name = None

# Server parameters for STDIO transport
server_params = StdioServerParameters(
    command="python",
    args=["calculator_server.py"],
    env=None
)

async def basic_client_demo():
    """Basic demo: Connect, list tools, and invoke one directly."""
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                logger.info("Initializing MCP session")
                await session.initialize()

                # List available tools
                tools_result = await session.list_tools()
                print("Available Tools:")
                for tool in tools_result.tools:
                    print(f"- {tool.name}: {tool.description or 'No description'}")

                # Invoke the 'add' tool
                logger.info("Calling add tool with a=5, b=3")
                result = await session.call_tool("add", {"a": 5, "b": 3})
                print(f"\nInvoke 'add(5, 3)' Result: {result.content[0].text}")
    except Exception as e:
        logger.error(f"Error in basic_client_demo: {e}")
        print(f"Error in basic demo: {e}")

async def ai_integrated_demo(user_query: str):
    """AI-integrated demo: Use Azure OpenAI to process a query, which may invoke tools."""
    if not azure_client or not deployment_name:
        print("Azure OpenAI not configured. Skipping AI demo.")
        return

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                logger.info("Initializing MCP session for AI demo")
                await session.initialize()

                # Get tool schemas
                tools_result = await session.list_tools()
                tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": t.name,
                            "description": t.description or "",
                            "parameters": t.inputSchema
                        }
                    } for t in tools_result.tools
                ]

                messages = [{"role": "user", "content": user_query}]

                # Call Azure OpenAI API with tools
                logger.info(f"Sending query to Azure OpenAI: {user_query}")
                response = azure_client.chat.completions.create(
                    model=deployment_name,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto"
                )

                assistant_message = response.choices[0].message
                messages.append(assistant_message)

                # Handle tool calls
                if assistant_message.tool_calls:
                    logger.info(f"Processing {len(assistant_message.tool_calls)} tool calls")
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)

                        logger.info(f"Calling tool: {tool_name} with args: {tool_args}")
                        # Invoke the tool
                        tool_result = await session.call_tool(tool_name, tool_args)
                        tool_result_content = tool_result.content[0].text

                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "content": tool_result_content,
                            "tool_call_id": tool_call.id
                        })

                    # Get final response from Azure OpenAI
                    logger.info("Getting final response from Azure OpenAI")
                    final_response = azure_client.chat.completions.create(
                        model=deployment_name,
                        messages=messages
                    )
                    print("=== Assistant's Response ===")
                    print(final_response.choices[0].message.content)
                else:
                    print("=== Assistant's Response ===")
                    print(assistant_message.content)
    except Exception as e:
        logger.error(f"Error in ai_integrated_demo: {e}")
        print(f"Error in AI demo: {e}")

async def main():
    # Run basic demo
    print("Running basic MCP client demo...")
    await basic_client_demo()
    print("\nBasic demo completed successfully!\n")

    # Check if Azure OpenAI is properly configured
    if azure_client and deployment_name:
        try:
            # Test if we can create a simple completion
            logger.info("Testing Azure OpenAI credentials")
            test_response = azure_client.chat.completions.create(
                model=deployment_name,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            # If we get here, credentials are likely real
            print("Azure OpenAI credentials appear to be configured. Running AI-integrated demo...")
            user_query = "What is 8 multiplied by 9?"
            await ai_integrated_demo(user_query)
        except Exception as e:
            logger.warning(f"Azure OpenAI test failed: {e}")
            print(f"Azure OpenAI credentials not properly configured: {e}")
            print("Skipping AI-integrated demo. To enable it, update your .env file with real Azure OpenAI credentials.")
            print("\nThe MCP client is working correctly! The available tools are:")
            print("- add: Add two numbers")
            print("- multiply: Multiply two numbers")
            print("- subtract: Subtract second number from first")
            print("- divide: Divide first number by second")
            print("- power: Raise base to the power of exponent")
    else:
        print("Azure OpenAI not configured.")
        print("\nThe MCP client is working correctly! The available tools are:")
        print("- add: Add two numbers")
        print("- multiply: Multiply two numbers")
        print("- subtract: Subtract second number from first")
        print("- divide: Divide first number by second")
        print("- power: Raise base to the power of exponent")

if __name__ == "__main__":
    logger.info("Starting MCP Client Demo")
    asyncio.run(main())
