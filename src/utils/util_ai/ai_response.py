import re
from typing import Dict, Any


def parse_review_text(text: str) -> Dict[str, Any]:
    section_pattern = r"\[(Issues|Recommendation(?:s)?|Rating|Conclusion)\]\n(.*?)(?=\n\[|$)"
    list_item_pattern = r"^\d+\.\s+(.*)"

    matches = re.findall(section_pattern, text, re.DOTALL)
    result = {}

    for section, content in matches:
        list_items = re.findall(list_item_pattern, content, re.MULTILINE)

        if list_items:
            result[section.lower()] = {i + 1: item for i, item in enumerate(list_items)}
        else:
            result[section.lower()] = content.strip()
    result["raw_text"] = text
    return result
