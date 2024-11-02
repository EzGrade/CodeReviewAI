"""
GitHub service
"""
import logging
from typing import Dict

from github import Auth
from github import Github as GithubAPI
from github.Repository import Repository

import config
from utils.util_redis.rd import RedisClient

logger = logging.getLogger(__name__)


class Github:
    """
    Class to interact with GitHub API
    """

    def __init__(
            self,
            owner: str,
            repo: str,
            force_reload: bool = False,
            github_api: GithubAPI = None
    ):
        self.owner = owner
        self.repo = repo
        self.redis_client = RedisClient()
        self.force_reload = force_reload
        self.auth = Auth.Token(token=config.GITHUB_TOKEN)
        self.g = github_api or GithubAPI(auth=self.auth)
        self.repository = self.get_repository()

    def get_repository(
            self
    ) -> Repository:
        """
        Get repository object
        :return:
        """
        return self.g.get_repo(f"{self.owner}/{self.repo}")

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
                logger.info(
                    "Repository files found in cache for repo: %s",
                    self.repository.full_name
                )
                return eval(cached_files)

        def get_files_recursively(path: str, ref: str) -> Dict[str, str]:
            """
            Get files recursively
            Means get files from the directory and subdirectories
            :param path:
            :param ref:
            :return:
            """
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
