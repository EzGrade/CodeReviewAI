import logging
from typing import Dict

from github import Auth, GithubIntegration

import config
from utils.util_redis.rd import RedisClient

logger = logging.getLogger(__name__)


class Github:
    def __init__(
            self,
            owner: str,
            repo: str,
            force_reload: bool = False
    ):
        self.redis_client = RedisClient()
        self.force_reload = force_reload
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
        cache_key = f"installation_id_{owner}"
        cached_id = self.redis_client.get(cache_key)
        if cached_id:
            logger.info(f"Installation ID found in cache for owner: {owner}")
            return int(cached_id)

        installations = self.app_client.get_installations()
        for installation in installations:
            _owner = installation.get_repos()[0].owner.login
            if _owner == owner:
                installation_id = installation.id
                self.redis_client.set(cache_key, installation_id, ex=config.REDIS_CACHE_EXPIRATION)
                return installation_id

        raise ValueError("Installation not found")

    def get_repository_files(
            self,
    ) -> Dict[str, str]:
        """
        Get content of the files in the main branch
        :return:
        """
        cache_key = f"repository_files_{self.repository.full_name}"
        if not self.force_reload:
            cached_files = self.redis_client.get(cache_key)
            if cached_files:
                logger.info(f"Repository files found in cache for repo: {self.repository.full_name}")
                return eval(cached_files)

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
        files = get_files_recursively("", main_branch_ref)
        self.redis_client.set(cache_key, str(files), ex=config.REDIS_CACHE_EXPIRATION)
        return files
