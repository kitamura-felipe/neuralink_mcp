import os
import json
from typing import Dict, Any, List, Optional
import aiohttp
from dotenv import load_dotenv

class NeuralinkClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NEURALINK_API_KEY")
        self.api_url = os.getenv("NEURALINK_API_URL")
        
        if not self.api_key or not self.api_url:
            raise ValueError("NEURALINK_API_KEY or NEURALINK_API_URL not found in environment variables")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def connect(self) -> Dict[str, Any]:
        """
        Establish connection with the Neuralink device.
        
        Returns:
            Dict[str, Any]: Connection status and device information
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/connect",
                    headers=self.headers
                ) as response:
                    return await response.json()
        except Exception as e:
            raise Exception(f"Error connecting to Neuralink: {str(e)}")

    async def read_neural_data(self, duration_ms: int = 1000) -> List[Dict[str, Any]]:
        """
        Read neural data from the device.
        
        Args:
            duration_ms (int): Duration to read data for in milliseconds
            
        Returns:
            List[Dict[str, Any]]: Neural data readings
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/read",
                    headers=self.headers,
                    params={"duration": duration_ms}
                ) as response:
                    return await response.json()
        except Exception as e:
            raise Exception(f"Error reading neural data: {str(e)}")

    async def send_stimulation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send stimulation pattern to the device.
        
        Args:
            pattern (Dict[str, Any]): Stimulation pattern configuration
            
        Returns:
            Dict[str, Any]: Response from the device
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/stimulate",
                    headers=self.headers,
                    json=pattern
                ) as response:
                    return await response.json()
        except Exception as e:
            raise Exception(f"Error sending stimulation: {str(e)}")

    async def get_device_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Neuralink device.
        
        Returns:
            Dict[str, Any]: Device status information
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/status",
                    headers=self.headers
                ) as response:
                    return await response.json()
        except Exception as e:
            raise Exception(f"Error getting device status: {str(e)}")

    async def disconnect(self) -> Dict[str, Any]:
        """
        Disconnect from the Neuralink device.
        
        Returns:
            Dict[str, Any]: Disconnection status
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/disconnect",
                    headers=self.headers
                ) as response:
                    return await response.json()
        except Exception as e:
            raise Exception(f"Error disconnecting from Neuralink: {str(e)}") 