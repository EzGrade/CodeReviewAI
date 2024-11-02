"""
Module to interact with OpenAI API (async version)
"""

from typing import List, Dict
import aiohttp
import asyncio
import json

import config
import logger

logger = logger.get_logger(__name__)


class OpenAi:
    """
    Class to interact with OpenAI API asynchronously
    """

    def __init__(
            self,
            context: List[Dict[str, str]],
            api_key: str = config.OPENAI_API_KEY,
            model: str = config.OPENAI_MODEL
    ):
        self.context = context
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def get_response(self) -> str:
        """
        Get response from OpenAI asynchronously
        :return response: OpenAI response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": self.context
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=headers, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                ai_message = data["choices"][0]["message"]["content"]
                logger.info("AI response: %s", ai_message)
                return ai_message
