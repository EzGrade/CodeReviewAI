"""
Environment utility functions
"""

import os


def get_env_var(
        key: str,
        default: str = None
) -> str:
    """
    Get environment variable
    :param key:
    :param default:
    :return:
    """
    try:
        return os.environ[key]
    except KeyError as e:
        if default is not None:
            return default
        raise RuntimeError(f"Environment variable {key} not set") from e
