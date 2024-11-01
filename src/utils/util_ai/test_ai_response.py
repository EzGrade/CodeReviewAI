from ai_response import parse_review_text


def test_parse_review_with_list_items():
    text = """
[Issues]
1. This is the first issue.
2. This is the second issue.

[Recommendations]
1. This is the first recommendation.
2. This is the second recommendation.

[Rating]
Some rating here.

[Conclusion]
Some conclusion here.
    """
    expected_result = {
        'issues': {
            1: 'This is the first issue.',
            2: 'This is the second issue.'
        },
        'recommendations': {
            1: 'This is the first recommendation.',
            2: 'This is the second recommendation.'
        },
        'rating': 'Some rating here.',
        'conclusion': 'Some conclusion here.',
        'raw_text': text
    }
    result = parse_review_text(text)
    assert result == expected_result


def test_parse_review_without_list_items():
    text = """
[Issues]
This is an issue without list items.

[Recommendations]
This is a recommendation without list items.

[Rating]
Some rating here.

[Conclusion]
Some conclusion here.
    """
    expected_result = {
        'issues': 'This is an issue without list items.',
        'recommendations': 'This is a recommendation without list items.',
        'rating': 'Some rating here.',
        'conclusion': 'Some conclusion here.',
        'raw_text': text
    }
    result = parse_review_text(text)
    assert result == expected_result


def test_parse_review_mixed_content():
    text = """
[Issues]
This is an issue without list items.

[Recommendations]
1. This is the first recommendation.
2. This is the second recommendation.

[Rating]
Some rating here.

[Conclusion]
Some conclusion here.
    """
    expected_result = {
        'issues': 'This is an issue without list items.',
        'recommendations': {
            1: 'This is the first recommendation.',
            2: 'This is the second recommendation.'
        },
        'rating': 'Some rating here.',
        'conclusion': 'Some conclusion here.',
        'raw_text': text
    }
    result = parse_review_text(text)
    assert result == expected_result
