"""
Module to interact with OpenAI API
"""

from typing import List, Dict

import openai

import config
import logger

logger = logger.get_logger(__name__)


class OpenAi:
    """
    Class to interact with OpenAI API
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
        self.client = self.get_openai_client()

    def get_openai_client(self):
        """
        Get OpenAI client
        :return:
        """
        return openai.OpenAI(
            api_key=self.api_key
        )

    def get_response(
            self,
    ) -> str:
        """
        Get response from OpenAI
        :return response: OpenAI response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.context
        )
        ai_message = response.choices[0].message.content
        logger.info("AI response: %s", ai_message)
        return ai_message
