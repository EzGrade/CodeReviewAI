from utils.environment import get_env_var

GITHUB_APP_ID = int(get_env_var("GITHUB_APP_ID", default=0))
GITHUB_PRIVATE_KEY = get_env_var("GITHUB_PRIVATE_KEY", default="")

LOGGING_LEVEL = get_env_var("LOGGING_LEVEL", default="DEBUG")
