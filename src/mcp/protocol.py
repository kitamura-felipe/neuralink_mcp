import asyncio
import json
from typing import Dict, Any, Optional, List
from ..llm.openai_client import OpenAIClient
from ..neuralink.neuralink_client import NeuralinkClient

class MCPProtocol:
    def __init__(self, llm_client: OpenAIClient, neuralink_client: NeuralinkClient):
        self.llm_client = llm_client
        self.neuralink_client = neuralink_client
        self.is_connected = False
        self.is_processing = False

    async def start_communication(self) -> None:
        """
        Start the communication between LLM and Neuralink.
        """
        try:
            # Connect to Neuralink device
            connection_status = await self.neuralink_client.connect()
            if connection_status.get("status") == "connected":
                self.is_connected = True
                print("Successfully connected to Neuralink device")
            else:
                raise Exception("Failed to connect to Neuralink device")

            # Start the main communication loop
            await self._communication_loop()

        except Exception as e:
            print(f"Error in communication: {str(e)}")
            await self.stop_communication()

    async def _communication_loop(self) -> None:
        """
        Main communication loop between LLM and Neuralink.
        """
        while self.is_connected:
            try:
                # Read neural data
                neural_data = await self.neuralink_client.read_neural_data()
                
                # Process neural data through LLM
                if neural_data:
                    self.is_processing = True
                    response = await self._process_neural_data(neural_data)
                    
                    # Send stimulation if needed
                    if response.get("should_stimulate"):
                        await self.neuralink_client.send_stimulation(
                            response["stimulation_pattern"]
                        )
                    
                    self.is_processing = False

                # Small delay to prevent overwhelming the system
                await asyncio.sleep(0.1)

            except Exception as e:
                print(f"Error in communication loop: {str(e)}")
                break

    async def _process_neural_data(self, neural_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process neural data through the LLM to generate appropriate responses.
        
        Args:
            neural_data (List[Dict[str, Any]]): Raw neural data from the device
            
        Returns:
            Dict[str, Any]: Processed response with stimulation pattern if needed
        """
        try:
            # Convert neural data to a format suitable for the LLM
            prompt = self._format_neural_data(neural_data)
            
            # Get LLM response
            llm_response = await self.llm_client.generate_response(prompt)
            
            # Parse LLM response and generate stimulation pattern
            return self._parse_llm_response(llm_response)
            
        except Exception as e:
            raise Exception(f"Error processing neural data: {str(e)}")

    def _format_neural_data(self, neural_data: List[Dict[str, Any]]) -> str:
        """
        Format neural data into a prompt for the LLM.
        
        Args:
            neural_data (List[Dict[str, Any]]): Raw neural data
            
        Returns:
            str: Formatted prompt
        """
        # Convert neural data to a structured format
        formatted_data = {
            "timestamp": neural_data[0].get("timestamp"),
            "readings": [reading.get("value") for reading in neural_data],
            "metadata": neural_data[0].get("metadata", {})
        }
        
        return f"Process the following neural data and determine if stimulation is needed: {json.dumps(formatted_data)}"

    def _parse_llm_response(self, llm_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse LLM response and generate stimulation pattern.
        
        Args:
            llm_response (Dict[str, Any]): Response from the LLM
            
        Returns:
            Dict[str, Any]: Processed response with stimulation pattern
        """
        try:
            # Parse the LLM's text response
            response_text = llm_response["text"]
            response_data = json.loads(response_text)
            
            return {
                "should_stimulate": response_data.get("should_stimulate", False),
                "stimulation_pattern": response_data.get("pattern", {}),
                "confidence": response_data.get("confidence", 0.0)
            }
            
        except json.JSONDecodeError:
            # If the response isn't valid JSON, return a safe default
            return {
                "should_stimulate": False,
                "stimulation_pattern": {},
                "confidence": 0.0
            }

    async def stop_communication(self) -> None:
        """
        Stop the communication and disconnect from the Neuralink device.
        """
        if self.is_connected:
            try:
                await self.neuralink_client.disconnect()
                self.is_connected = False
                print("Successfully disconnected from Neuralink device")
            except Exception as e:
                print(f"Error disconnecting from Neuralink: {str(e)}") 