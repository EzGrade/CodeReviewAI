from typing import List, Dict

import config


class Prompt:
    def __init__(
            self,
            assignment: Dict[str, str],
            files_content: Dict[str, str],
            candidate_level: str,
            system_prompt: str = config.PROMPT
    ):
        self.system_prompt = system_prompt
        self.assignment = assignment
        self.files_content = files_content
        self.candidate_level = candidate_level

    def files_to_dict(self):
        messages = []
        for file_name, file_content in self.files_content.items():
            content = f"File: {file_name}\n{file_content}"
            context_prompt_message = {
                "role": "user",
                "content": content,
            }
            messages.append(context_prompt_message)
        return messages

    def get_prompt(self):
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
        messages.append(candidate_level_message)
        messages.extend(self.files_to_dict())
        return messages
