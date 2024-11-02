"""
This module contains the Pydantic model for the Review object.
"""

from pydantic import BaseModel


class Review(BaseModel):
    """
    Basic body model for the Review object.
    """
    assignment_description: str
    github_repo_url: str
    candidate_level: str
    repository_force_reload_files: bool = False
