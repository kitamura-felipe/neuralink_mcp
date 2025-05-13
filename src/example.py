import asyncio
import os
from dotenv import load_dotenv
from llm.openai_client import OpenAIClient
from neuralink.neuralink_client import NeuralinkClient
from mcp.protocol import MCPProtocol

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize clients
    llm_client = OpenAIClient()
    neuralink_client = NeuralinkClient()
    
    # Create MCP protocol instance
    mcp = MCPProtocol(llm_client, neuralink_client)
    
    try:
        # Start communication
        print("Starting communication between LLM and Neuralink...")
        await mcp.start_communication()
        
    except KeyboardInterrupt:
        print("\nStopping communication...")
        await mcp.stop_communication()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await mcp.stop_communication()

if __name__ == "__main__":
    asyncio.run(main()) 