from typing import List, Dict, Optional
from app.models.classroom import Classroom

class ClassroomService:
    def __init__(self):
        self.classrooms: Dict[str, Classroom] = {}
    
    def add_classroom(self, classroom: Classroom) -> Classroom:
        """
        Add a new classroom
        """
        self.classrooms[classroom.id] = classroom
        return classroom
    
    def get_classroom(self, classroom_id: str) -> Optional[Classroom]:
        """
        Get a classroom by ID
        """
        return self.classrooms.get(classroom_id)
    
    def get_all_classrooms(self) -> List[Classroom]:
        """
        Get all classrooms
        """
        return list(self.classrooms.values())
    
    def update_classroom(self, classroom_id: str, updated_classroom: Classroom) -> Optional[Classroom]:
        """
        Update an existing classroom
        """
        if classroom_id in self.classrooms:
            self.classrooms[classroom_id] = updated_classroom
            return updated_classroom
        return None
    
    def delete_classroom(self, classroom_id: str) -> bool:
        """
        Delete a classroom by ID
        """
        if classroom_id in self.classrooms:
            del self.classrooms[classroom_id]
            return True
        return False
    
    def set_classroom_status(self, classroom_id: str, status: str) -> Optional[Classroom]:
        """
        Set the status of a classroom (available/unavailable)
        """
        if classroom_id in self.classrooms:
            self.classrooms[classroom_id].status = status
            return self.classrooms[classroom_id]
        return None
    
    def get_available_classrooms(self) -> List[Classroom]:
        """
        Get all available classrooms
        """
        return [classroom for classroom in self.classrooms.values() if classroom.status == "available"]
    
    def get_classrooms_by_capacity(self, min_capacity: int) -> List[Classroom]:
        """
        Get classrooms with capacity greater than or equal to min_capacity
        """
        return [classroom for classroom in self.classrooms.values() if classroom.capacity >= min_capacity]
    
    def assign_department_preference(self, classroom_id: str, department_code: str) -> Optional[Classroom]:
        """
        Assign a department preference to a classroom
        """
        if classroom_id in self.classrooms:
            classroom = self.classrooms[classroom_id]
            # If equipment field is used for department preferences
            if classroom.equipment:
                classroom.equipment += f",{department_code}"
            else:
                classroom.equipment = department_code
            return classroom
        return None
    
    def get_classroom_utilization_report(self) -> Dict[str, any]:
        """
        Generate a report on classroom utilization
        """
        total_classrooms = len(self.classrooms)
        available_classrooms = len(self.get_available_classrooms())
        unavailable_classrooms = total_classrooms - available_classrooms
        
        # Calculate capacity statistics
        total_capacity = sum(classroom.capacity for classroom in self.classrooms.values())
        avg_capacity = total_capacity / total_classrooms if total_classrooms > 0 else 0
        
        return {
            "total_classrooms": total_classrooms,
            "available_classrooms": available_classrooms,
            "unavailable_classrooms": unavailable_classrooms,
            "total_capacity": total_capacity,
            "average_capacity": avg_capacity,
            "utilization_rate": (unavailable_classrooms / total_classrooms * 100) if total_classrooms > 0 else 0
        }