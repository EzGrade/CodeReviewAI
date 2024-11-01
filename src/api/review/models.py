from pydantic import BaseModel


class Review(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: str
    repository_force_reload_files: bool = False
