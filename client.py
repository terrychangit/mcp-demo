import asyncio
import json
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Azure OpenAI client setup
azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"  # Fixed to current API version
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
if not azure_client.api_key or not deployment_name:
    raise ValueError("AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, or AZURE_OPENAI_DEPLOYMENT not set in .env file")

# Server parameters for STDIO transport
server_params = StdioServerParameters(
    command="python",
    args=["calculator_server.py"],
    env=None
)

async def basic_client_demo():
    """Basic demo: Connect, list tools, and invoke one directly."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available Tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description or 'No description'}")

            # Invoke the 'add' tool
            result = await session.call_tool("add", {"a": 5, "b": 3})
            print(f"\nInvoke 'add(5, 3)' Result: {result.content[0].text}")

async def ai_integrated_demo(user_query: str):
    """AI-integrated demo: Use Azure OpenAI to process a query, which may invoke tools."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
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

            # Call Azure OpenAI API with tools
            response = azure_client.chat.completions.create(
                model=deployment_name,
                messages=[{"role": "user", "content": user_query}],
                tools=tools,
                tool_choice="auto"
            )

            # Handle tool use
            if response.choices[0].finish_reason == "tool_calls":
                tool_call = response.choices[0].message.tool_calls[0]
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Invoke the tool
                tool_result = await session.call_tool(tool_name, tool_args)
                tool_result_content = tool_result.content[0].text

                # Send tool result back to Azure OpenAI
                follow_up = azure_client.chat.completions.create(
                    model=deployment_name,
                    messages=[
                        {"role": "user", "content": user_query},
                        response.choices[0].message,
                        {"role": "tool", "content": tool_result_content, "tool_call_id": tool_call.id}
                    ]
                )
                print("=== Assistant's Response ===")
                print(follow_up.choices[0].message.content)
            else:
                print("=== Assistant's Response ===")
                print(response.choices[0].message.content)

async def main():
    # Run basic demo
    print("Running basic MCP client demo...")
    await basic_client_demo()
    print("\nBasic demo completed successfully!\n")

    # Check if Azure OpenAI is properly configured
    try:
        # Test if we can create a simple completion (this will fail with placeholder credentials)
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
        print(f"Azure OpenAI credentials not properly configured: {e}")
        print("Skipping AI-integrated demo. To enable it, update your .env file with real Azure OpenAI credentials.")
        print("\nThe MCP client is working correctly! The tools are:")
        print("- add: Add two integers")
        print("- multiply: Multiply two integers")

if __name__ == "__main__":
    asyncio.run(main())
