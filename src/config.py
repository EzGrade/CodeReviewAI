from utils.util_environment.environment import get_env_var

LOGGING_LEVEL = get_env_var("LOGGING_LEVEL", default="DEBUG")

GITHUB_APP_ID = int(get_env_var("GITHUB_APP_ID"))
GITHUB_PRIVATE_KEY = get_env_var("GITHUB_PRIVATE_KEY")

if GITHUB_PRIVATE_KEY.endswith(".pem"):
    try:
        with open(GITHUB_PRIVATE_KEY, "r", encoding="utf-8") as key_file:
            GITHUB_PRIVATE_KEY = key_file.read()
    except FileNotFoundError:
        if LOGGING_LEVEL == "DEBUG":
            pass
        else:
            raise

OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
OPENAI_MODEL = get_env_var("OPENAI_MODEL", default="gpt-3.5-turbo")

PROMPT_PATH = get_env_var("PROMPT_PATH", default="src/prompt.txt")
with open(PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
    PROMPT = prompt_file.read()
