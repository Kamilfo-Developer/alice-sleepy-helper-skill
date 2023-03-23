from typing import Literal
from skill.db.repos.base_repo import BaseRepo
from skill.db.repos.sa_repo import SARepo
from skill.db.sa_db_settings import sa_repo_config


def get_repo(repo_type: Literal["sa"]) -> BaseRepo:
    match repo_type:
        case "sa":
            return SARepo(sa_repo_config)
