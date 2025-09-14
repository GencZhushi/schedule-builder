from typing import List, Dict, Optional
from app.models.time_slot import TimeSlot, TimeSlotConfiguration
from datetime import datetime, time

class TimeSlotService:
    def __init__(self):
        self.time_slots: Dict[str, TimeSlot] = {}
        self.configuration = TimeSlotConfiguration()
    
    def add_time_slot(self, time_slot: TimeSlot) -> TimeSlot:
        """
        Add a new time slot
        """
        self.time_slots[time_slot.id] = time_slot
        return time_slot
    
    def get_time_slot(self, time_slot_id: str) -> Optional[TimeSlot]:
        """
        Get a time slot by ID
        """
        return self.time_slots.get(time_slot_id)
    
    def get_all_time_slots(self) -> List[TimeSlot]:
        """
        Get all time slots
        """
        return list(self.time_slots.values())
    
    def update_time_slot(self, time_slot_id: str, updated_time_slot: TimeSlot) -> Optional[TimeSlot]:
        """
        Update an existing time slot
        """
        if time_slot_id in self.time_slots:
            self.time_slots[time_slot_id] = updated_time_slot
            return updated_time_slot
        return None
    
    def delete_time_slot(self, time_slot_id: str) -> bool:
        """
        Delete a time slot by ID
        """
        if time_slot_id in self.time_slots:
            del self.time_slots[time_slot_id]
            return True
        return False
    
    def set_time_slot_status(self, time_slot_id: str, status: str) -> Optional[TimeSlot]:
        """
        Set the status of a time slot (available/unavailable)
        """
        if time_slot_id in self.time_slots:
            self.time_slots[time_slot_id].status = status
            return self.time_slots[time_slot_id]
        return None
    
    def get_available_time_slots(self) -> List[TimeSlot]:
        """
        Get all available time slots
        """
        return [time_slot for time_slot in self.time_slots.values() if time_slot.status == "available"]
    
    def get_time_slots_by_day(self, day: str) -> List[TimeSlot]:
        """
        Get all time slots for a specific day
        """
        return [time_slot for time_slot in self.time_slots.values() if time_slot.day.lower() == day.lower()]
    
    def get_time_slots_by_duration(self, duration: int) -> List[TimeSlot]:
        """
        Get all time slots with a specific duration
        """
        return [time_slot for time_slot in self.time_slots.values() if time_slot.duration == duration]
    
    def create_standard_time_slots(self) -> List[TimeSlot]:
        """
        Create standard time slots based on configuration
        """
        created_slots = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        # Create time slots for each day
        for day in days:
            # Morning slots (9:00-11:00)
            morning_start = "09:00"
            morning_end = "11:00"
            morning_slot = TimeSlot(
                id=f"{day.lower()}_morning",
                day=day,
                start_time=morning_start,
                end_time=morning_end,
                duration=120,  # 2 hours in minutes
                status="available"
            )
            self.add_time_slot(morning_slot)
            created_slots.append(morning_slot)
            
            # Midday slots (11:00-15:00)
            midday_start = "11:00"
            midday_end = "15:00"
            midday_slot = TimeSlot(
                id=f"{day.lower()}_midday",
                day=day,
                start_time=midday_start,
                end_time=midday_end,
                duration=240,  # 4 hours in minutes
                status="available"
            )
            self.add_time_slot(midday_slot)
            created_slots.append(midday_slot)
            
            # Evening slots (15:00-17:00)
            evening_start = "15:00"
            evening_end = "17:00"
            evening_slot = TimeSlot(
                id=f"{day.lower()}_evening",
                day=day,
                start_time=evening_start,
                end_time=evening_end,
                duration=120,  # 2 hours in minutes
                status="available"
            )
            self.add_time_slot(evening_slot)
            created_slots.append(evening_slot)
        
        return created_slots
    
    def get_time_slot_utilization_report(self) -> Dict[str, any]:
        """
        Generate a report on time slot utilization
        """
        total_time_slots = len(self.time_slots)
        available_time_slots = len(self.get_available_time_slots())
        unavailable_time_slots = total_time_slots - available_time_slots
        
        # Group time slots by day
        slots_by_day = {}
        for time_slot in self.time_slots.values():
            if time_slot.day not in slots_by_day:
                slots_by_day[time_slot.day] = []
            slots_by_day[time_slot.day].append(time_slot)
        
        return {
            "total_time_slots": total_time_slots,
            "available_time_slots": available_time_slots,
            "unavailable_time_slots": unavailable_time_slots,
            "utilization_rate": (unavailable_time_slots / total_time_slots * 100) if total_time_slots > 0 else 0,
            "slots_by_day": {day: len(slots) for day, slots in slots_by_day.items()}
        }
    
    def assign_department_preference(self, time_slot_id: str, department_code: str) -> Optional[TimeSlot]:
        """
        Assign a department preference to a time slot
        """
        if time_slot_id in self.time_slots:
            # In a real implementation, we might store this in a separate field or table
            # For now, we'll just return the time slot
            return self.time_slots[time_slot_id]
        return None
    
    def get_configuration(self) -> TimeSlotConfiguration:
        """
        Get the time slot configuration
        """
        return self.configuration
    
    def update_configuration(self, config: TimeSlotConfiguration) -> TimeSlotConfiguration:
        """
        Update the time slot configuration
        """
        self.configuration = config
        return self.configuration