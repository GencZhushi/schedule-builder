from typing import List, Dict, Set, Tuple
from app.models.schedule import Schedule
from app.models.lecture import Lecture
from app.models.classroom import Classroom
from app.services.time_slot_service import TimeSlotService
import json

class ConflictDetector:
    def __init__(self, time_slot_service: TimeSlotService):
        self.time_slot_service = time_slot_service
    
    def detect_all_conflicts(self, schedules: List[Schedule], lectures: List[Lecture]) -> Dict[str, List]:
        """
        Detect all types of conflicts in the schedule
        """
        conflicts = {
            "classroom_conflicts": [],
            "professor_conflicts": [],
            "group_conflicts": [],
            "time_slot_conflicts": [],
            "lecture_exercise_conflicts": [],
            "capacity_conflicts": [],
            "departmental_conflicts": []
        }
        
        # Detect each type of conflict
        conflicts["classroom_conflicts"] = self.detect_classroom_conflicts(schedules)
        conflicts["professor_conflicts"] = self.detect_professor_conflicts(schedules)
        conflicts["group_conflicts"] = self.detect_group_conflicts(schedules, lectures)
        conflicts["time_slot_conflicts"] = self.detect_time_slot_conflicts(schedules, lectures)
        conflicts["lecture_exercise_conflicts"] = self.detect_lecture_exercise_conflicts(schedules, lectures)
        conflicts["capacity_conflicts"] = self.detect_capacity_conflicts(schedules, lectures)
        conflicts["departmental_conflicts"] = self.detect_departmental_conflicts(schedules, lectures)
        
        return conflicts
    
    def detect_classroom_conflicts(self, schedules: List[Schedule]) -> List[Dict]:
        """
        Detect conflicts where the same classroom is booked for multiple lectures at the same time
        """
        classroom_usage = {}
        conflicts = []
        
        for schedule in schedules:
            key = (schedule.classroom_id, schedule.time_slot_id)
            if key in classroom_usage:
                # Conflict found
                conflicts.append({
                    "type": "classroom_conflict",
                    "classroom_id": schedule.classroom_id,
                    "time_slot_id": schedule.time_slot_id,
                    "conflicting_schedules": [classroom_usage[key].id, schedule.id],
                    "description": f"Classroom {schedule.classroom_id} double-booked at time slot {schedule.time_slot_id}"
                })
            else:
                classroom_usage[key] = schedule
        
        return conflicts
    
    def detect_professor_conflicts(self, schedules: List[Schedule]) -> List[Dict]:
        """
        Detect conflicts where the same professor is scheduled to teach multiple lectures at the same time
        """
        professor_usage = {}
        conflicts = []
        
        for schedule in schedules:
            key = (schedule.professor, schedule.time_slot_id)
            if key in professor_usage:
                # Conflict found
                conflicts.append({
                    "type": "professor_conflict",
                    "professor": schedule.professor,
                    "time_slot_id": schedule.time_slot_id,
                    "conflicting_schedules": [professor_usage[key].id, schedule.id],
                    "description": f"Professor {schedule.professor} double-booked at time slot {schedule.time_slot_id}"
                })
            else:
                professor_usage[key] = schedule
        
        return conflicts
    
    def detect_group_conflicts(self, schedules: List[Schedule], lectures: List[Lecture]) -> List[Dict]:
        """
        Detect conflicts where the same student group is scheduled for multiple lectures at the same time
        """
        # Create lecture lookup
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        
        group_usage = {}
        conflicts = []
        
        for schedule in schedules:
            lecture = lecture_dict.get(schedule.lecture_id)
            if not lecture:
                continue
                
            # Handle main group
            main_group = self._extract_main_group(lecture.grup_rreg)
            key = (main_group, schedule.time_slot_id)
            
            if key in group_usage:
                # Conflict found
                conflicts.append({
                    "type": "group_conflict",
                    "group": main_group,
                    "time_slot_id": schedule.time_slot_id,
                    "conflicting_schedules": [group_usage[key].id, schedule.id],
                    "description": f"Group {main_group} double-booked at time slot {schedule.time_slot_id}"
                })
            else:
                group_usage[key] = schedule
            
            # Handle subgroup if it exists
            if '.' in lecture.grup_rreg:
                subgroup = lecture.grup_rreg
                sub_key = (subgroup, schedule.time_slot_id)
                
                if sub_key in group_usage:
                    # Conflict found
                    conflicts.append({
                        "type": "subgroup_conflict",
                        "subgroup": subgroup,
                        "time_slot_id": schedule.time_slot_id,
                        "conflicting_schedules": [group_usage[sub_key].id, schedule.id],
                        "description": f"Subgroup {subgroup} double-booked at time slot {schedule.time_slot_id}"
                    })
                else:
                    group_usage[sub_key] = schedule
        
        return conflicts
    
    def detect_time_slot_conflicts(self, schedules: List[Schedule], lectures: List[Lecture]) -> List[Dict]:
        """
        Detect conflicts related to time slot constraints
        """
        # Create lecture lookup
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        
        conflicts = []
        
        for schedule in schedules:
            lecture = lecture_dict.get(schedule.lecture_id)
            if not lecture:
                continue
            
            time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
            if not time_slot:
                conflicts.append({
                    "type": "time_slot_conflict",
                    "schedule_id": schedule.id,
                    "issue": "invalid_time_slot",
                    "description": f"Schedule {schedule.id} references invalid time slot {schedule.time_slot_id}"
                })
                continue
            
            # Check if lecture duration fits in time slot
            if time_slot.duration < lecture.time_per_lec_rreg:
                conflicts.append({
                    "type": "time_slot_conflict",
                    "schedule_id": schedule.id,
                    "issue": "insufficient_duration",
                    "description": f"Lecture {lecture.lenda_e_rreg} duration ({lecture.time_per_lec_rreg} min) exceeds time slot {time_slot.id} duration ({time_slot.duration} min)"
                })
        
        return conflicts
    
    def detect_lecture_exercise_conflicts(self, schedules: List[Schedule], lectures: List[Lecture]) -> List[Dict]:
        """
        Detect conflicts where exercises are scheduled before their corresponding lectures
        """
        # Create lecture lookup
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        
        # Separate lectures and exercises
        lecture_schedules = {}
        exercise_schedules = {}
        
        for schedule in schedules:
            lecture = lecture_dict.get(schedule.lecture_id)
            if not lecture:
                continue
                
            if lecture.status_lende_rreg == 'L':
                lecture_schedules[lecture.lenda_e_rreg] = schedule
            elif lecture.status_lende_rreg == 'U':
                exercise_schedules[lecture.lenda_e_rreg] = schedule
        
        conflicts = []
        
        # Check if exercises are scheduled after lectures
        for exercise_name, exercise_schedule in exercise_schedules.items():
            if exercise_name in lecture_schedules:
                lecture_schedule = lecture_schedules[exercise_name]
                
                # In a more sophisticated implementation, we would compare actual time slots
                # For now, we'll just note that both exist
                pass
            else:
                conflicts.append({
                    "type": "lecture_exercise_conflict",
                    "exercise": exercise_name,
                    "issue": "missing_lecture",
                    "description": f"Exercise {exercise_name} scheduled without corresponding lecture"
                })
        
        return conflicts
    
    def detect_capacity_conflicts(self, schedules: List[Schedule], lectures: List[Lecture]) -> List[Dict]:
        """
        Detect conflicts where classroom capacity is insufficient
        """
        # This would require access to classroom data which is not passed to this method
        # In a full implementation, we would check classroom capacity against expected attendance
        return []
    
    def detect_departmental_conflicts(self, schedules: List[Schedule], lectures: List[Lecture]) -> List[Dict]:
        """
        Detect conflicts related to departmental scheduling preferences
        """
        # Create lecture lookup
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        
        # Group schedules by department
        dept_schedules = {}
        
        for schedule in schedules:
            lecture = lecture_dict.get(schedule.lecture_id)
            if not lecture:
                continue
                
            dept = lecture.dep_reale_rreg
            if dept not in dept_schedules:
                dept_schedules[dept] = []
            dept_schedules[dept].append((schedule, lecture))
        
        conflicts = []
        
        # Check for departmental cohesion issues
        for dept, dept_scheds in dept_schedules.items():
            if len(dept_scheds) < 2:
                continue
                
            # Count days used by this department
            days_used = set()
            for schedule, lecture in dept_scheds:
                time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
                if time_slot:
                    days_used.add(time_slot.day)
            
            # If lectures are spread across too many days, flag as potential cohesion issue
            if len(days_used) > 3 and len(dept_scheds) > 5:
                conflicts.append({
                    "type": "departmental_conflict",
                    "department": dept,
                    "days_used": list(days_used),
                    "lecture_count": len(dept_scheds),
                    "issue": "poor_cohesion",
                    "description": f"Department {dept} lectures spread across {len(days_used)} days (may affect cohesion)"
                })
        
        return conflicts
    
    def _extract_main_group(self, group_id: str) -> str:
        """
        Extract main group from subgroup (e.g., "Gr. 1.1" -> "Gr. 1")
        """
        if '.' in group_id:
            parts = group_id.split('.')
            return f"{parts[0]}.{parts[1]}"
        return group_id
    
    def generate_conflict_report(self, conflicts: Dict[str, List]) -> Dict[str, any]:
        """
        Generate a formatted conflict report
        """
        total_conflicts = sum(len(conflict_list) for conflict_list in conflicts.values())
        
        report = {
            "total_conflicts": total_conflicts,
            "conflict_breakdown": {
                "classroom_conflicts": len(conflicts["classroom_conflicts"]),
                "professor_conflicts": len(conflicts["professor_conflicts"]),
                "group_conflicts": len(conflicts["group_conflicts"]),
                "time_slot_conflicts": len(conflicts["time_slot_conflicts"]),
                "lecture_exercise_conflicts": len(conflicts["lecture_exercise_conflicts"]),
                "capacity_conflicts": len(conflicts["capacity_conflicts"]),
                "departmental_conflicts": len(conflicts["departmental_conflicts"])
            },
            "conflicts": conflicts,
            "severity": self._assess_conflict_severity(total_conflicts)
        }
        
        return report
    
    def _assess_conflict_severity(self, total_conflicts: int) -> str:
        """
        Assess the severity of conflicts
        """
        if total_conflicts == 0:
            return "none"
        elif total_conflicts <= 5:
            return "low"
        elif total_conflicts <= 15:
            return "medium"
        else:
            return "high"
    
    def get_conflict_summary(self, conflicts: Dict[str, List]) -> str:
        """
        Generate a summary of conflicts as a string
        """
        total = sum(len(conflict_list) for conflict_list in conflicts.values())
        if total == 0:
            return "No conflicts detected."
        
        summary = f"Total conflicts: {total}\n"
        for conflict_type, conflict_list in conflicts.items():
            if conflict_list:
                summary += f"- {conflict_type.replace('_', ' ').title()}: {len(conflict_list)}\n"
        
        return summary