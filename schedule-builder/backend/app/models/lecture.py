from pydantic import BaseModel
from typing import Optional, List

class Lecture(BaseModel):
    id: Optional[str] = None
    lenda_e_rreg: str  # Name of the lecture/course
    dep_reale_rreg: str  # Department offering the lecture
    sem_rreg: str  # Semester when the lecture is offered
    niveli_rreg: str  # Academic level (Bachelor/Master)
    viti_rreg: str  # Academic year
    prof_rreg: str  # Professor teaching the lecture
    grup_rreg: str  # Student group (e.g., Gr. 1, Gr. 2)
    status_lende_rreg: str  # Lecture type (L = Lecture, U = Exercise)
    qasja_lende_rreg: str  # Course requirement (O = Obligatory, Z = Elective)
    mesimdhe_lende_rreg: str  # Instructor type (P = Professor, A = Teaching Assistant)
    time_per_lec_rreg: int  # Length of lecture in minutes (45, 90, 135)
    time_preference: Optional[str] = None  # Preferred time slot (Morning, Midday, Evening)
    related_lecture: Optional[str] = None  # Reference to related lecture (L->U relationship)