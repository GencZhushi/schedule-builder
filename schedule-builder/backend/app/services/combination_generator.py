from typing import List, Dict, Tuple, Any
from app.models.lecture import Lecture
from app.models.classroom import Classroom
from app.models.time_slot import TimeSlot
from app.models.schedule import Schedule
from app.services.classroom_service import ClassroomService
from app.services.time_slot_service import TimeSlotService
import itertools
import uuid

class CombinationGenerator:
    def __init__(self, classroom_service: ClassroomService, time_slot_service: TimeSlotService):
        self.classroom_service = classroom_service
        self.time_slot_service = time_slot_service
    
    def generate_combinations(self, lectures: List[Lecture]) -> List[Dict[str, Any]]:
        """
        Generate all possible combinations of lectures with classrooms and time slots
        """
        combinations = []
        
        # Get available classrooms and time slots
        available_classrooms = self.classroom_service.get_available_classrooms()
        available_time_slots = self.time_slot_service.get_available_time_slots()
        
        # Generate combinations for each lecture
        for lecture in lectures:
            lecture_combinations = self._generate_lecture_combinations(
                lecture, available_classrooms, available_time_slots
            )
            combinations.extend(lecture_combinations)
        
        return combinations
    
    def _generate_lecture_combinations(self, lecture: Lecture, 
                                     classrooms: List[Classroom], 
                                     time_slots: List[TimeSlot]) -> List[Dict[str, Any]]:
        """
        Generate combinations for a single lecture
        """
        combinations = []
        
        # Filter classrooms by capacity
        suitable_classrooms = [
            classroom for classroom in classrooms 
            if classroom.capacity >= 30  # Assuming a minimum capacity
        ]
        
        # Filter time slots by duration
        suitable_time_slots = [
            time_slot for time_slot in time_slots 
            if time_slot.duration >= lecture.time_per_lec_rreg
        ]
        
        # Create all possible combinations
        for classroom in suitable_classrooms:
            for time_slot in suitable_time_slots:
                combination = {
                    'lecture_id': lecture.id,
                    'classroom_id': classroom.id,
                    'time_slot_id': time_slot.id,
                    'professor': lecture.prof_rreg,
                    'score': self._calculate_combination_score(lecture, classroom, time_slot)
                }
                combinations.append(combination)
        
        # Sort combinations by score (higher is better)
        combinations.sort(key=lambda x: x['score'], reverse=True)
        
        return combinations
    
    def _calculate_combination_score(self, lecture: Lecture, classroom: Classroom, time_slot: TimeSlot) -> float:
        """
        Calculate a score for a combination based on various factors
        """
        score = 0.0
        
        # Factor 1: Time preference match (if specified)
        if lecture.time_preference:
            if self._matches_time_preference(lecture.time_preference, time_slot):
                score += 10.0
        
        # Factor 2: Lecture duration fit
        if time_slot.duration >= lecture.time_per_lec_rreg:
            # Bonus for exact match or minimal excess
            duration_diff = time_slot.duration - lecture.time_per_lec_rreg
            if duration_diff == 0:
                score += 5.0
            elif duration_diff <= 45:  # Within 45 minutes
                score += 3.0
            else:
                score += 1.0
        
        # Factor 3: Classroom capacity efficiency
        capacity_utilization = lecture.time_per_lec_rreg / classroom.capacity
        if 0.5 <= capacity_utilization <= 0.9:
            score += 5.0  # Good utilization
        elif capacity_utilization > 0.9:
            score += 2.0  # High utilization
        else:
            score += 1.0  # Low utilization
        
        # Factor 4: Course requirement timing
        if lecture.qasja_lende_rreg == 'Z':  # Elective
            # Prefer morning and evening for electives
            if time_slot.id.endswith('_morning') or time_slot.id.endswith('_evening'):
                score += 3.0
        elif lecture.qasja_lende_rreg == 'O':  # Obligatory
            # Prefer midday for obligatory courses
            if time_slot.id.endswith('_midday'):
                score += 3.0
        
        return score
    
    def _matches_time_preference(self, preference: str, time_slot: TimeSlot) -> bool:
        """
        Check if a time slot matches the lecture's time preference
        """
        if preference.lower() == "morning" and time_slot.id.endswith('_morning'):
            return True
        elif preference.lower() == "midday" and time_slot.id.endswith('_midday'):
            return True
        elif preference.lower() == "evening" and time_slot.id.endswith('_evening'):
            return True
        return False
    
    def generate_lecture_exercise_pairs(self, lectures: List[Lecture]) -> List[Tuple[Lecture, Lecture]]:
        """
        Generate pairs of lectures and corresponding exercises
        """
        pairs = []
        lectures_dict = {lecture.lenda_e_rreg: lecture for lecture in lectures 
                        if lecture.status_lende_rreg == 'L'}
        exercises_dict = {lecture.lenda_e_rreg: lecture for lecture in lectures 
                         if lecture.status_lende_rreg == 'U'}
        
        # Pair lectures with their corresponding exercises
        for lecture_name, lecture in lectures_dict.items():
            if lecture_name in exercises_dict:
                pairs.append((lecture, exercises_dict[lecture_name]))
        
        return pairs
    
    def create_combination_matrix(self, lectures: List[Lecture]) -> Dict[str, Any]:
        """
        Create a matrix of possible scheduling options
        """
        # Get available resources
        classrooms = self.classroom_service.get_available_classrooms()
        time_slots = self.time_slot_service.get_available_time_slots()
        
        # Create matrix structure
        matrix = {
            'lectures': [],
            'classrooms': [classroom.id for classroom in classrooms],
            'time_slots': [time_slot.id for time_slot in time_slots],
            'combinations': []
        }
        
        # Add lecture information
        for lecture in lectures:
            matrix['lectures'].append({
                'id': lecture.id,
                'name': lecture.lenda_e_rreg,
                'type': lecture.status_lende_rreg,
                'duration': lecture.time_per_lec_rreg
            })
        
        # Generate combinations
        combinations = self.generate_combinations(lectures)
        matrix['combinations'] = combinations[:100]  # Limit to first 100 for performance
        
        return matrix
    
    def filter_valid_combinations(self, combinations: List[Dict[str, Any]], 
                                constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter combinations based on constraints
        """
        valid_combinations = []
        
        for combination in combinations:
            if self._satisfies_constraints(combination, constraints):
                valid_combinations.append(combination)
        
        return valid_combinations
    
    def _satisfies_constraints(self, combination: Dict[str, Any], 
                             constraints: Dict[str, Any]) -> bool:
        """
        Check if a combination satisfies given constraints
        """
        # This is a simplified implementation
        # In a real system, this would check against various scheduling constraints
        
        # Example constraints that could be checked:
        # - Professor availability
        # - Classroom capacity
        # - Time slot availability
        # - Lecture duration fit
        # - Departmental cohesion
        # - Group scheduling conflicts
        
        # For now, we'll assume all generated combinations are valid
        return True