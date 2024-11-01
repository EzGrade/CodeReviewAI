import logging
from typing import Dict

from github import Auth, GithubIntegration

import config

logger = logging.getLogger(__name__)


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
        for installation in installations:
            _owner = installation.get_repos()[0].owner.login
            if _owner == owner:
                return installation.id
        raise ValueError("Installation not found")

    def get_repository_files(
            self,
    ) -> Dict[str, str]:
        """
        Get content of the files in the main branch
        :return:
        """

        def get_files_recursively(path: str, ref: str) -> Dict[str, str]:
            files = self.repository.get_contents(path, ref=ref)
            context = {}
            for file in files:
                if file.type == "dir":
                    context.update(get_files_recursively(file.path, ref))
                else:
                    context[file.path] = file.decoded_content.decode("utf-8")
            return context

        main_branch_ref = self.repository.default_branch
        return get_files_recursively("", main_branch_ref)
