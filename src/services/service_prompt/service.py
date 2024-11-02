"""
This module contains Prompt service.
It allows to generate prompt messages for AI context.
"""

from typing import List, Dict

import config


class Prompt:
    """
    Class to generate prompt messages for AI context
    """

    def __init__(
            self,
            assignment: str,
            files_content: Dict[str, str],
            candidate_level: str,
            system_prompt: str = config.PROMPT
    ):
        self.system_prompt = system_prompt
        self.assignment = assignment
        self.files_content = files_content
        self.candidate_level = candidate_level

    def files_to_dict(self) -> List[Dict[str, str]]:
        """
        Convert files content to list of messages
        :return:
        """
        messages = []
        for file_name, file_content in self.files_content.items():
            content = f"File: {file_name}\n{file_content}"
            context_prompt_message = {
                "role": "user",
                "content": content,
            }
            messages.append(context_prompt_message)
        return messages

    def get_prompt(self) -> List[Dict[str, str]]:
        """
        Get prompt messages
        :return:
        """
        messages: List[Dict[str, str]] = []
        system_prompt_message: Dict[str, str] = {
            "role": "system",
            "content": self.system_prompt,
        }
        assignment_message: Dict[str, str] = {
            "role": "system",
            "content": f"Assignment: {self.assignment}"
        }
        candidate_level_message: Dict[str, str] = {
            "role": "system",
            "content": f"Programmer Level: {self.candidate_level}"
        }
        messages.append(system_prompt_message)
        messages.append(assignment_message)
        messages.append(candidate_level_message)
        messages.extend(self.files_to_dict())
        return messages
