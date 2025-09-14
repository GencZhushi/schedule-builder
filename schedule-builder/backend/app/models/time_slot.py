from pydantic import BaseModel
from typing import Optional
from datetime import time

class TimeSlot(BaseModel):
    id: str  # Unique identifier
    day: str  # Day of the week (Monday-Friday)
    start_time: str  # Start time (e.g., 09:00)
    end_time: str  # End time (e.g., 17:00)
    duration: int  # Duration in minutes
    status: str = "available"  # Available/Unavailable

class TimeSlotConfiguration(BaseModel):
    minimum_slot: int = 45  # Minimum time slot (45 minutes)
    standard_slot: int = 90  # Standard time slot (90 minutes)
    extended_slot: int = 135  # Extended time slot (135 minutes)
    working_hours_start: str = "09:00"  # Start of working hours (09:00)
    working_hours_end: str = "17:00"  # End of working hours (17:00)
    morning_start: str = "09:00"  # Start of morning period (09:00)
    morning_end: str = "11:00"  # End of morning period (11:00)
    midday_start: str = "11:00"  # Start of midday period (11:00)
    midday_end: str = "15:00"  # End of midday period (15:00)
    evening_start: str = "15:00"  # Start of evening period (15:00)
    evening_end: str = "17:00"  # End of evening period (17:00)