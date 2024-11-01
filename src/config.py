from utils.environment import get_env_var

GITHUB_APP_ID = int(get_env_var("GITHUB_APP_ID", default=0))
GITHUB_PRIVATE_KEY = get_env_var("GITHUB_PRIVATE_KEY", default="")
if GITHUB_PRIVATE_KEY.endswith(".pem"):
    with open(GITHUB_PRIVATE_KEY, "r", encoding="utf-8") as key_file:
        GITHUB_PRIVATE_KEY = key_file.read()

OPENAI_API_KEY = get_env_var("OPENAI_API_KEY", default="")
OPENAI_MODEL = get_env_var("OPENAI_MODEL", default="gpt-3.5-turbo")

PROMPT_PATH = get_env_var("PROMPT_PATH", default="src/prompt.txt")
with open(PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
    PROMPT = prompt_file.read()

LOGGING_LEVEL = get_env_var("LOGGING_LEVEL", default="DEBUG")
