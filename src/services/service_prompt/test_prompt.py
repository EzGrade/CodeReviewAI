"""
This module contains tests for the Prompt class.
"""

import pytest
from services.service_prompt.service import Prompt


@pytest.fixture
def prompt_obj():
    """
    Create a Prompt instance for testing
    :return:
    """
    assignment = {"task": "Implement a feature"}
    files_content = {
        "file1.py": "print('Hello, World!')",
        "file2.py": "def add(a, b): return a + b"
    }
    candidate_level = "Junior"
    system_prompt = "This is a system prompt."

    return Prompt(
        assignment=assignment,
        files_content=files_content,
        candidate_level=candidate_level,
        system_prompt=system_prompt
    )


def test_files_to_dict(prompt_obj):
    """
    Test files_to_dict method
    :param prompt_obj:
    :return:
    """
    expected_messages = [
        {
            "role": "user",
            "content": "File: file1.py\nprint('Hello, World!')"
        },
        {
            "role": "user",
            "content": "File: file2.py\ndef add(a, b): return a + b"
        }
    ]
    assert prompt_obj.files_to_dict() == expected_messages


def test_get_prompt(prompt_obj):
    """
    Test get_prompt method
    :param prompt_obj:
    :return:
    """
    expected_messages = [
        {
            "role": "system",
            "content": "This is a system prompt."
        },
        {
            "role": "system",
            "content": "Programmer Level: Junior"
        },
        {
            "role": "user",
            "content": "File: file1.py\nprint('Hello, World!')"
        },
        {
            "role": "user",
            "content": "File: file2.py\ndef add(a, b): return a + b"
        }
    ]
    assert prompt_obj.get_prompt() == expected_messages
