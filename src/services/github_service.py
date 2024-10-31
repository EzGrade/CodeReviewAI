from github import Auth, GithubIntegration

import config


class Github:
    def __init__(
            self,
            owner: str,
            repo: str,
    ):
        self.auth = Auth.AppAuth(
            app_id=config.GITHUB_APP_ID,
            private_key=config.GITHUB_PRIVATE_KEY,
        )

        self.app_client = GithubIntegration(auth=self.auth)

