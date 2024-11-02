"""
GitHub service (async version)
"""
import base64
import logging
from typing import Dict

import httpx
import json
from config import GITHUB_TOKEN, REDIS_CACHE_EXPIRATION
from utils.util_redis.rd import RedisClient

logger = logging.getLogger(__name__)


class Github:
    """
    Class to interact with GitHub API
    """

    BASE_URL = "https://api.github.com"

    def __init__(
            self,
            owner: str,
            repo: str,
            force_reload: bool = False
    ):
        self.owner = owner
        self.repo = repo
        self.redis_client = RedisClient()
        self.force_reload = force_reload
        self.auth_headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    async def get_repository(self) -> Dict:
        """
        Get repository information
        :return:
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{self.owner}/{self.repo}",
                headers=self.auth_headers
            )
            response.raise_for_status()
            return response.json()

    async def get_repository_files(self) -> Dict[str, str]:
        """
        Get content of the files in the main branch
        :return:
        """
        cache_key = f"repository_files_{self.owner}_{self.repo}"
        if not self.force_reload:
            cached_files = await self.redis_client.get(cache_key)
            if cached_files:
                logger.info(
                    "Repository files found in cache for repo: %s/%s",
                    self.owner, self.repo
                )
                return json.loads(cached_files)

        async def get_files_recursively(path: str, ref: str) -> Dict[str, str]:
            """
            Get files recursively
            Means get files from the directory and subdirectories
            :param path:
            :param ref:
            :return:
            """
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/repos/{self.owner}/{self.repo}/contents/{path}",
                    headers=self.auth_headers,
                    params={"ref": ref}
                )
                response.raise_for_status()
                files = response.json()

            context = {}
            for file in files:
                if file["type"] == "dir":
                    context.update(await get_files_recursively(file["path"], ref))
                else:
                    file_content = await self.get_file_content(file["path"], ref)
                    context[file["path"]] = file_content
            return context

        repo_info = await self.get_repository()
        main_branch_ref = repo_info["default_branch"]
        files = await get_files_recursively("", main_branch_ref)
        await self.redis_client.set(cache_key, json.dumps(files), ex=REDIS_CACHE_EXPIRATION)
        return files

    async def get_file_content(self, path: str, ref: str) -> str:
        """
        Get the content of a file by path and ref
        :param path:
        :param ref:
        :return:
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{self.owner}/{self.repo}/contents/{path}",
                headers=self.auth_headers,
                params={"ref": ref}
            )
            response.raise_for_status()
            file_data = response.json()
            return base64.b64decode(file_data["content"]).decode("utf-8")
