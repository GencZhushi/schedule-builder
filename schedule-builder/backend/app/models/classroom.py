from pydantic import BaseModel
from typing import Optional

class Classroom(BaseModel):
    id: str  # Unique identifier (e.g., S1, S2, S3)
    name: str  # Classroom name
    capacity: int  # Number of students that can be accommodated
    equipment: Optional[str] = None  # Special equipment available
    status: str = "available"  # Available/Unavailable