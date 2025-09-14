from pydantic import BaseModel
from typing import Optional

class Subgroup(BaseModel):
    id: str  # Subgroup identifier (e.g., Gr. 1.1, Gr. 1.2)
    parent_group: str  # Parent group identifier
    lecture_count: int = 0  # Number of lectures for subgroup
    daily_limit: int = 3  # Maximum lectures per day for subgroup