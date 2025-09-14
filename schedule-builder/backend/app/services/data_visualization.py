from typing import List, Dict, Any
from app.models.lecture import Lecture
from app.models.department import Department
from app.models.group import Group
from app.models.subgroup import Subgroup
from app.models.schedule import Schedule
import json

class DataVisualizationService:
    def __init__(self):
        pass
    
    def generate_lecture_statistics(self, lectures: List[Lecture]) -> Dict[str, Any]:
        """
        Generate statistics about lectures
        """
        if not lectures:
            return {}
        
        # Count by lecture type
        lecture_count = sum(1 for l in lectures if l.status_lende_rreg == 'L')
        exercise_count = sum(1 for l in lectures if l.status_lende_rreg == 'U')
        
        # Count by requirement type
        obligatory_count = sum(1 for l in lectures if l.qasja_lende_rreg == 'O')
        elective_count = sum(1 for l in lectures if l.qasja_lende_rreg == 'Z')
        
        # Count by instructor type
        professor_count = sum(1 for l in lectures if l.mesimdhe_lende_rreg == 'P')
        assistant_count = sum(1 for l in lectures if l.mesimdhe_lende_rreg == 'A')
        
        # Count by duration
        duration_counts = {}
        for lecture in lectures:
            duration = lecture.time_per_lec_rreg
            if duration not in duration_counts:
                duration_counts[duration] = 0
            duration_counts[duration] += 1
        
        # Count by department
        dept_counts = {}
        for lecture in lectures:
            dept = lecture.dep_reale_rreg
            if dept not in dept_counts:
                dept_counts[dept] = 0
            dept_counts[dept] += 1
        
        # Count by semester
        semester_counts = {}
        for lecture in lectures:
            semester = lecture.sem_rreg
            if semester not in semester_counts:
                semester_counts[semester] = 0
            semester_counts[semester] += 1
        
        return {
            "total_lectures": len(lectures),
            "lecture_types": {
                "lectures": lecture_count,
                "exercises": exercise_count
            },
            "requirements": {
                "obligatory": obligatory_count,
                "elective": elective_count
            },
            "instructors": {
                "professors": professor_count,
                "assistants": assistant_count
            },
            "durations": duration_counts,
            "departments": dept_counts,
            "semesters": semester_counts
        }
    
    def generate_department_analysis(self, departments: List[Department], 
                                  lectures: List[Lecture]) -> Dict[str, Any]:
        """
        Generate departmental analysis
        """
        dept_analysis = {}
        
        # Create lecture lookup by department
        dept_lectures = {}
        for lecture in lectures:
            dept = lecture.dep_reale_rreg
            if dept not in dept_lectures:
                dept_lectures[dept] = []
            dept_lectures[dept].append(lecture)
        
        for department in departments:
            dept_code = department.code
            dept_lectures_list = dept_lectures.get(dept_code, [])
            
            # Calculate statistics for this department
            lecture_count = len(dept_lectures_list)
            
            # Count by level
            bachelor_count = sum(1 for l in dept_lectures_list if l.niveli_rreg in ['Bachelor', 'Baçelor'])
            master_count = sum(1 for l in dept_lectures_list if l.niveli_rreg == 'Master')
            
            # Count by year
            year1_count = sum(1 for l in dept_lectures_list if l.viti_rreg == 'VITI I')
            year2_count = sum(1 for l in dept_lectures_list if l.viti_rreg == 'VITI II')
            
            dept_analysis[dept_code] = {
                "name": department.name,
                "lecture_count": lecture_count,
                "levels": {
                    "bachelor": bachelor_count,
                    "master": master_count
                },
                "years": {
                    "year1": year1_count,
                    "year2": year2_count
                },
                "cohesion_priority": department.cohesion_priority
            }
        
        return dept_analysis
    
    def generate_group_analysis(self, groups: List[Group], subgroups: List[Subgroup], 
                             lectures: List[Lecture]) -> Dict[str, Any]:
        """
        Generate group and subgroup analysis
        """
        # Create lecture lookup by group
        group_lectures = {}
        for lecture in lectures:
            group_id = lecture.grup_rreg
            # Extract main group if it's a subgroup
            main_group = group_id.split('.')[0] + '.' + group_id.split('.')[1] if '.' in group_id else group_id
            
            if main_group not in group_lectures:
                group_lectures[main_group] = []
            group_lectures[main_group].append(lecture)
        
        group_analysis = {}
        
        # Analyze main groups
        for group in groups:
            group_id = group.id
            group_lectures_list = group_lectures.get(group_id, [])
            
            # Count lectures
            lecture_count = len(group_lectures_list)
            
            # Count subgroups
            subgroup_count = len(group.sub_groups)
            
            group_analysis[group_id] = {
                "lecture_count": lecture_count,
                "subgroup_count": subgroup_count,
                "daily_limit": group.daily_limit,
                "subgroups": group.sub_groups
            }
        
        # Analyze subgroups
        subgroup_analysis = {}
        for subgroup in subgroups:
            subgroup_id = subgroup.id
            # Find lectures for this subgroup
            subgroup_lectures = [l for l in lectures if l.grup_rreg == subgroup_id]
            
            subgroup_analysis[subgroup_id] = {
                "lecture_count": len(subgroup_lectures),
                "parent_group": subgroup.parent_group,
                "daily_limit": subgroup.daily_limit
            }
        
        return {
            "groups": group_analysis,
            "subgroups": subgroup_analysis
        }
    
    def generate_time_preference_analysis(self, lectures: List[Lecture]) -> Dict[str, Any]:
        """
        Generate analysis of time preferences
        """
        # Count by time preference
        preference_counts = {"morning": 0, "midday": 0, "evening": 0, "unspecified": 0}
        
        for lecture in lectures:
            if lecture.time_preference:
                pref = lecture.time_preference.lower()
                if pref in preference_counts:
                    preference_counts[pref] += 1
                else:
                    preference_counts["unspecified"] += 1
            else:
                preference_counts["unspecified"] += 1
        
        # Count by requirement and time preference
        requirement_preference = {
            "obligatory": {"morning": 0, "midday": 0, "evening": 0, "unspecified": 0},
            "elective": {"morning": 0, "midday": 0, "evening": 0, "unspecified": 0}
        }
        
        for lecture in lectures:
            req_type = "obligatory" if lecture.qasja_lende_rreg == 'O' else "elective"
            if lecture.time_preference:
                pref = lecture.time_preference.lower()
                if pref in requirement_preference[req_type]:
                    requirement_preference[req_type][pref] += 1
                else:
                    requirement_preference[req_type]["unspecified"] += 1
            else:
                requirement_preference[req_type]["unspecified"] += 1
        
        return {
            "preferences": preference_counts,
            "requirement_preferences": requirement_preference
        }
    
    def generate_lecture_exercise_relationships(self, lectures: List[Lecture]) -> Dict[str, Any]:
        """
        Analyze relationships between lectures and exercises
        """
        # Separate lectures and exercises
        pure_lectures = {l.lenda_e_rreg: l for l in lectures if l.status_lende_rreg == 'L'}
        exercises = {l.lenda_e_rreg: l for l in lectures if l.status_lende_rreg == 'U'}
        
        # Find pairs
        pairs = []
        unpaired_lectures = []
        unpaired_exercises = []
        
        for lecture_name, lecture in pure_lectures.items():
            if lecture_name in exercises:
                pairs.append({
                    "lecture": lecture_name,
                    "lecture_professor": lecture.prof_rreg,
                    "exercise_professor": exercises[lecture_name].prof_rreg,
                    "same_professor": lecture.prof_rreg == exercises[lecture_name].prof_rreg
                })
            else:
                unpaired_lectures.append(lecture_name)
        
        for exercise_name, exercise in exercises.items():
            if exercise_name not in pure_lectures:
                unpaired_exercises.append(exercise_name)
        
        return {
            "paired_count": len(pairs),
            "unpaired_lectures_count": len(unpaired_lectures),
            "unpaired_exercises_count": len(unpaired_exercises),
            "pairs": pairs,
            "unpaired_lectures": unpaired_lectures,
            "unpaired_exercises": unpaired_exercises
        }
    
    def generate_daily_load_analysis(self, schedules: List[Schedule], 
                                  time_slot_service) -> Dict[str, Any]:
        """
        Analyze daily lecture load
        """
        # Group schedules by day
        day_schedules = {}
        
        for schedule in schedules:
            time_slot = time_slot_service.get_time_slot(schedule.time_slot_id)
            if time_slot:
                day = time_slot.day
                if day not in day_schedules:
                    day_schedules[day] = []
                day_schedules[day].append(schedule)
        
        # Calculate statistics
        daily_stats = {}
        for day, day_scheds in day_schedules.items():
            daily_stats[day] = {
                "lecture_count": len(day_scheds),
                "classrooms_used": len(set(s.classroom_id for s in day_scheds))
            }
        
        return {
            "daily_load": daily_stats,
            "total_lectures": sum(stats["lecture_count"] for stats in daily_stats.values()),
            "average_per_day": sum(stats["lecture_count"] for stats in daily_stats.values()) / len(daily_stats) if daily_stats else 0
        }
    
    def generate_conflict_report(self, conflicts: List[str]) -> Dict[str, Any]:
        """
        Generate a formatted conflict report
        """
        return {
            "conflict_count": len(conflicts),
            "conflicts": conflicts
        }
    
    def generate_summary_dashboard(self, parsed_data: Dict[str, Any], 
                                schedules: List[Schedule], conflicts: List[str],
                                time_slot_service) -> Dict[str, Any]:
        """
        Generate a comprehensive dashboard summary
        """
        lectures = parsed_data.get('lectures', [])
        departments = parsed_data.get('departments', [])
        groups = parsed_data.get('groups', [])
        subgroups = parsed_data.get('subgroups', [])
        
        summary = {
            "lecture_statistics": self.generate_lecture_statistics(lectures),
            "department_analysis": self.generate_department_analysis(departments, lectures),
            "group_analysis": self.generate_group_analysis(groups, subgroups, lectures),
            "time_preference_analysis": self.generate_time_preference_analysis(lectures),
            "lecture_exercise_relationships": self.generate_lecture_exercise_relationships(lectures),
            "daily_load_analysis": self.generate_daily_load_analysis(schedules, time_slot_service),
            "conflict_report": self.generate_conflict_report(conflicts)
        }
        
        return summary
    
    def export_dashboard_data(self, dashboard_data: Dict[str, Any]) -> str:
        """
        Export dashboard data as JSON string
        """
        return json.dumps(dashboard_data, indent=2, default=str)