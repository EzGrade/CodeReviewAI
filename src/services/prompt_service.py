from typing import List, Dict


class Prompt:
    def __init__(
            self,
            system_prompt: str,
            files_content: Dict[str, str]
    ):
        self.system_prompt = system_prompt
        self.files_content = files_content

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
        messages.append(system_prompt_message)
        messages.extend(self.files_to_dict())
        return messages
