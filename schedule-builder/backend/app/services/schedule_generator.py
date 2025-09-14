from typing import List, Dict, Set, Tuple
from app.models.lecture import Lecture
from app.models.classroom import Classroom
from app.models.time_slot import TimeSlot
from app.models.schedule import Schedule
from app.models.group import Group
from app.models.subgroup import Subgroup
from app.services.classroom_service import ClassroomService
from app.services.time_slot_service import TimeSlotService
from app.services.combination_generator import CombinationGenerator
import uuid
from datetime import datetime

class ScheduleGenerator:
    def __init__(self, classroom_service: ClassroomService, time_slot_service: TimeSlotService):
        self.classroom_service = classroom_service
        self.time_slot_service = time_slot_service
        self.combination_generator = CombinationGenerator(classroom_service, time_slot_service)
        self.schedules: List[Schedule] = []
    
    def generate_schedule(self, lectures: List[Lecture], groups: List[Group], 
                         subgroups: List[Subgroup]) -> Tuple[List[Schedule], List[str]]:
        """
        Generate a schedule with constraint checking
        Returns a tuple of (schedules, conflicts)
        """
        conflicts = []
        generated_schedules = []
        
        # Sort lectures by priority (exercises after lectures, electives at edges)
        sorted_lectures = self._sort_lectures(lectures)
        
        # Track resource usage
        used_classrooms: Dict[str, Set[str]] = {}  # classroom_id -> set of time_slot_ids
        professor_schedule: Dict[str, Set[str]] = {}  # professor -> set of time_slot_ids
        group_schedule: Dict[str, Set[str]] = {}  # group -> set of time_slot_ids
        subgroup_schedule: Dict[str, Set[str]] = {}  # subgroup -> set of time_slot_ids
        
        # Initialize tracking structures
        for classroom in self.classroom_service.get_all_classrooms():
            used_classrooms[classroom.id] = set()
        
        for lecture in lectures:
            if lecture.prof_rreg not in professor_schedule:
                professor_schedule[lecture.prof_rreg] = set()
            
            # Handle main group
            main_group = self._extract_main_group(lecture.grup_rreg)
            if main_group not in group_schedule:
                group_schedule[main_group] = set()
            
            # Handle subgroup if it exists
            if '.' in lecture.grup_rreg:
                if lecture.grup_rreg not in subgroup_schedule:
                    subgroup_schedule[lecture.grup_rreg] = set()
        
        # Generate schedule for each lecture
        for lecture in sorted_lectures:
            schedule, conflict = self._schedule_lecture(
                lecture, used_classrooms, professor_schedule, 
                group_schedule, subgroup_schedule
            )
            
            if schedule:
                generated_schedules.append(schedule)
                # Update tracking structures
                self._update_tracking_structures(
                    schedule, lecture, used_classrooms, 
                    professor_schedule, group_schedule, subgroup_schedule
                )
            elif conflict:
                conflicts.append(conflict)
        
        return generated_schedules, conflicts
    
    def _sort_lectures(self, lectures: List[Lecture]) -> List[Lecture]:
        """
        Sort lectures by priority:
        1. Obligatory lectures (midday)
        2. Elective lectures (morning/evening)
        3. Obligatory exercises (midday)
        4. Elective exercises (morning/evening)
        """
        def sort_key(lecture: Lecture):
            # Primary sort: lectures before exercises
            is_lecture = 0 if lecture.status_lende_rreg == 'L' else 1
            
            # Secondary sort: obligatory before electives
            is_obligatory = 0 if lecture.qasja_lende_rreg == 'O' else 1
            
            # Tertiary sort: time preference
            time_pref = 1  # midday default
            if lecture.time_preference:
                if lecture.time_preference.lower() == 'morning':
                    time_pref = 0
                elif lecture.time_preference.lower() == 'evening':
                    time_pref = 2
            
            return (is_lecture, is_obligatory, time_pref)
        
        return sorted(lectures, key=sort_key)
    
    def _extract_main_group(self, group_id: str) -> str:
        """
        Extract main group from subgroup (e.g., "Gr. 1.1" -> "Gr. 1")
        """
        if '.' in group_id:
            parts = group_id.split('.')
            return f"{parts[0]}.{parts[1]}"
        return group_id
    
    def _schedule_lecture(self, lecture: Lecture, 
                         used_classrooms: Dict[str, Set[str]],
                         professor_schedule: Dict[str, Set[str]],
                         group_schedule: Dict[str, Set[str]],
                         subgroup_schedule: Dict[str, Set[str]]) -> Tuple[Schedule, str]:
        """
        Schedule a single lecture, returning (schedule, conflict_message)
        """
        # Generate possible combinations
        combinations = self.combination_generator._generate_lecture_combinations(
            lecture,
            self.classroom_service.get_available_classrooms(),
            self.time_slot_service.get_available_time_slots()
        )
        
        # Try each combination until we find one that works
        for combination in combinations:
            classroom_id = combination['classroom_id']
            time_slot_id = combination['time_slot_id']
            
            # Check constraints
            conflict = self._check_constraints(
                lecture, classroom_id, time_slot_id,
                used_classrooms, professor_schedule,
                group_schedule, subgroup_schedule
            )
            
            if not conflict:
                # Create schedule
                schedule = Schedule(
                    id=str(uuid.uuid4()),
                    lecture_id=lecture.id,
                    time_slot_id=time_slot_id,
                    classroom_id=classroom_id,
                    professor=lecture.prof_rreg,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                return schedule, None
        
        # If we get here, no valid combination was found
        return None, f"No valid schedule found for lecture '{lecture.lenda_e_rreg}'"
    
    def _check_constraints(self, lecture: Lecture, 
                          classroom_id: str, time_slot_id: str,
                          used_classrooms: Dict[str, Set[str]],
                          professor_schedule: Dict[str, Set[str]],
                          group_schedule: Dict[str, Set[str]],
                          subgroup_schedule: Dict[str, Set[str]]) -> str:
        """
        Check all scheduling constraints
        Returns conflict message or None if no conflict
        """
        # Constraint 1: Classroom availability
        if time_slot_id in used_classrooms.get(classroom_id, set()):
            return f"Classroom {classroom_id} already booked for time slot {time_slot_id}"
        
        # Constraint 2: Professor availability
        if time_slot_id in professor_schedule.get(lecture.prof_rreg, set()):
            return f"Professor {lecture.prof_rreg} already teaching at time slot {time_slot_id}"
        
        # Constraint 3: Group availability
        main_group = self._extract_main_group(lecture.grup_rreg)
        if time_slot_id in group_schedule.get(main_group, set()):
            return f"Group {main_group} already has lecture at time slot {time_slot_id}"
        
        # Constraint 4: Subgroup availability (if applicable)
        if '.' in lecture.grup_rreg:
            if time_slot_id in subgroup_schedule.get(lecture.grup_rreg, set()):
                return f"Subgroup {lecture.grup_rreg} already has lecture at time slot {time_slot_id}"
        
        # Constraint 5: Classroom capacity
        classroom = self.classroom_service.get_classroom(classroom_id)
        if classroom and classroom.capacity < 30:  # Assuming minimum 30 students
            return f"Classroom {classroom_id} capacity ({classroom.capacity}) too small"
        
        # Constraint 6: Time slot duration
        time_slot = self.time_slot_service.get_time_slot(time_slot_id)
        if time_slot and time_slot.duration < lecture.time_per_lec_rreg:
            return f"Time slot {time_slot_id} duration ({time_slot.duration}) too short for lecture ({lecture.time_per_lec_rreg})"
        
        # Constraint 7: Lecture-Exercise ordering (simplified check)
        if lecture.status_lende_rreg == 'U':  # Exercise
            # In a full implementation, we would check if the corresponding lecture
            # is scheduled before this exercise
            pass
        
        return None  # No conflicts
    
    def _update_tracking_structures(self, schedule: Schedule, lecture: Lecture,
                                  used_classrooms: Dict[str, Set[str]],
                                  professor_schedule: Dict[str, Set[str]],
                                  group_schedule: Dict[str, Set[str]],
                                  subgroup_schedule: Dict[str, Set[str]]):
        """
        Update tracking structures after scheduling a lecture
        """
        # Update classroom usage
        if schedule.classroom_id not in used_classrooms:
            used_classrooms[schedule.classroom_id] = set()
        used_classrooms[schedule.classroom_id].add(schedule.time_slot_id)
        
        # Update professor schedule
        if schedule.professor not in professor_schedule:
            professor_schedule[schedule.professor] = set()
        professor_schedule[schedule.professor].add(schedule.time_slot_id)
        
        # Update group schedule
        main_group = self._extract_main_group(lecture.grup_rreg)
        if main_group not in group_schedule:
            group_schedule[main_group] = set()
        group_schedule[main_group].add(schedule.time_slot_id)
        
        # Update subgroup schedule if applicable
        if '.' in lecture.grup_rreg:
            if lecture.grup_rreg not in subgroup_schedule:
                subgroup_schedule[lecture.grup_rreg] = set()
            subgroup_schedule[lecture.grup_rreg].add(schedule.time_slot_id)
    
    def get_schedule_conflicts(self, schedules: List[Schedule]) -> List[str]:
        """
        Check for conflicts in an existing schedule
        """
        conflicts = []
        
        # Check for classroom conflicts
        classroom_usage = {}
        for schedule in schedules:
            key = (schedule.classroom_id, schedule.time_slot_id)
            if key in classroom_usage:
                conflicts.append(
                    f"Classroom conflict: {schedule.classroom_id} "
                    f"double-booked at time slot {schedule.time_slot_id}"
                )
            else:
                classroom_usage[key] = schedule.lecture_id
        
        # Check for professor conflicts
        professor_usage = {}
        for schedule in schedules:
            key = (schedule.professor, schedule.time_slot_id)
            if key in professor_usage:
                conflicts.append(
                    f"Professor conflict: {schedule.professor} "
                    f"double-booked at time slot {schedule.time_slot_id}"
                )
            else:
                professor_usage[key] = schedule.lecture_id
        
        return conflicts
    
    def get_departmental_cohesion_report(self, schedules: List[Schedule], 
                                       lectures: List[Lecture]) -> Dict[str, any]:
        """
        Generate a report on departmental cohesion
        """
        dept_schedules = {}
        
        # Group schedules by department
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        
        for schedule in schedules:
            if schedule.lecture_id in lecture_dict:
                lecture = lecture_dict[schedule.lecture_id]
                dept = lecture.dep_reale_rreg
                
                if dept not in dept_schedules:
                    dept_schedules[dept] = []
                dept_schedules[dept].append(schedule)
        
        # Calculate cohesion metrics
        cohesion_report = {}
        for dept, dept_scheds in dept_schedules.items():
            # Count how many lectures are scheduled on the same days
            days_used = set()
            for schedule in dept_scheds:
                time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
                if time_slot:
                    days_used.add(time_slot.day)
            
            cohesion_report[dept] = {
                'lecture_count': len(dept_scheds),
                'days_used': list(days_used),
                'days_count': len(days_used),
                'cohesion_score': len(dept_scheds) / len(days_used) if days_used else 0
            }
        
        return cohesion_report