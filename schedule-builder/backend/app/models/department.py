from pydantic import BaseModel
from typing import Optional, List

class Department(BaseModel):
    code: str  # Department code (AEM, EK, BF, MXH, Kon)
    name: str  # Full department name
    lecture_count: int = 0  # Number of lectures in department
    preferred_time_slots: Optional[str] = None  # Preferred time slots for department
    cohesion_priority: int = 0  # Priority for grouping lectures together