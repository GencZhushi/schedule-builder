from pydantic import BaseModel
from typing import Optional, List

class Group(BaseModel):
    id: str  # Group identifier (e.g., Gr. 1, Gr. 2)
    sub_groups: List[str] = []  # List of subgroups (e.g., Gr. 1.1, Gr. 1.2)
    lecture_count: int = 0  # Number of lectures for group
    daily_limit: int = 5  # Maximum lectures per day for group