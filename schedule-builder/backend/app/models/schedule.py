from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Schedule(BaseModel):
    id: Optional[str] = None
    lecture_id: str  # Reference to lecture
    time_slot_id: str  # Reference to time slot
    classroom_id: str  # Assigned classroom
    professor: str  # Assigned professor
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None