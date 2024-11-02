"""
This module contains the configuration for the application.
"""

from utils.util_environment.environment import get_env_var

LOGGING_LEVEL = get_env_var("LOGGING_LEVEL", default="DEBUG")

GITHUB_TOKEN = get_env_var("GITHUB_TOKEN")

OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
OPENAI_MODEL = get_env_var("OPENAI_MODEL", default="gpt-3.5-turbo")

PROMPT_PATH = get_env_var("PROMPT_PATH", default="src/prompt.txt")
with open(PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
    PROMPT = prompt_file.read()

REDIS_HOST = get_env_var("REDIS_HOST", default="redis")
REDIS_PORT = get_env_var("REDIS_PORT", default="6379")
REDIS_PASSWORD = get_env_var("REDIS_PASSWORD", default="")
REDIS_DB = get_env_var("REDIS_DB", default="0")
REDIS_CACHE_EXPIRATION = int(get_env_var("REDIS_CACHE_EXPIRATION", default="3600"))
