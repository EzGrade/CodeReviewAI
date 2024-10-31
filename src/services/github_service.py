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
        self.installation_id = self.get_installation_id(owner)
        self.client = self.app_client.get_github_for_installation(
            installation_id=self.installation_id,
        )
        self.repository = self.client.get_repo(f"{owner}/{repo}")

    def get_installation_id(
            self,
            owner: str,
    ) -> int:
        """
        Get installation id for the repository
        :param owner:
        :return:
        """
        installations = self.app_client.get_installations()
        for page in installations:
            for installation in page:
                if installation.account.login == owner:
                    return installation.id
        raise RuntimeError("Installation not found")
