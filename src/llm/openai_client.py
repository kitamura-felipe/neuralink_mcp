import os
from typing import Dict, Any, Optional
import openai
from dotenv import load_dotenv

class OpenAIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
        self.model = "gpt-4"  # Default model

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate a response from the OpenAI model.
        
        Args:
            prompt (str): The input prompt for the model
            **kwargs: Additional parameters for the API call
            
        Returns:
            Dict[str, Any]: The model's response
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return {
                "text": response.choices[0].message.content,
                "model": response.model,
                "usage": response.usage
            }
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def set_model(self, model: str) -> None:
        """
        Set the model to use for generation.
        
        Args:
            model (str): The model identifier
        """
        self.model = model

    async def stream_response(self, prompt: str, **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream responses from the OpenAI model.
        
        Args:
            prompt (str): The input prompt for the model
            **kwargs: Additional parameters for the API call
            
        Yields:
            Dict[str, Any]: Chunks of the model's response
        """
        try:
            async for chunk in await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                **kwargs
            ):
                if chunk.choices[0].delta.content:
                    yield {
                        "text": chunk.choices[0].delta.content,
                        "model": chunk.model
                    }
        except Exception as e:
            raise Exception(f"Error streaming response: {str(e)}") 