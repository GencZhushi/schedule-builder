from typing import List, Dict, Tuple, Set
from app.models.lecture import Lecture
from app.models.schedule import Schedule
from app.models.group import Group
from app.models.department import Department
from app.models.time_slot import TimeSlot
from app.services.schedule_generator import ScheduleGenerator
from app.services.classroom_service import ClassroomService
from app.services.time_slot_service import TimeSlotService
import random
import copy

class ScheduleOptimizer:
    def __init__(self, classroom_service: ClassroomService, time_slot_service: TimeSlotService):
        self.classroom_service = classroom_service
        self.time_slot_service = time_slot_service
        self.schedule_generator = ScheduleGenerator(classroom_service, time_slot_service)
    
    def optimize_schedule(self, schedules: List[Schedule], lectures: List[Lecture], 
                         groups: List[Group], departments: List[Department]) -> List[Schedule]:
        """
        Optimize an existing schedule to improve various metrics
        """
        # Make a copy of the schedules to work with
        optimized_schedules = copy.deepcopy(schedules)
        
        # Apply various optimization techniques
        optimized_schedules = self._optimize_departmental_cohesion(optimized_schedules, lectures)
        optimized_schedules = self._optimize_workload_balance(optimized_schedules, lectures)
        optimized_schedules = self._optimize_classroom_utilization(optimized_schedules)
        optimized_schedules = self._optimize_daily_distribution(optimized_schedules, lectures)
        
        return optimized_schedules
    
    def _optimize_departmental_cohesion(self, schedules: List[Schedule], 
                                     lectures: List[Lecture]) -> List[Schedule]:
        """
        Optimize for departmental cohesion (grouping lectures from same department together)
        """
        # Group lectures by department
        dept_lectures = {}
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        
        for schedule in schedules:
            if schedule.lecture_id in lecture_dict:
                lecture = lecture_dict[schedule.lecture_id]
                dept = lecture.dep_reale_rreg
                
                if dept not in dept_lectures:
                    dept_lectures[dept] = []
                dept_lectures[dept].append((schedule, lecture))
        
        # For each department, try to group lectures on fewer days
        optimized_schedules = schedules.copy()
        
        for dept, dept_scheds in dept_lectures.items():
            if len(dept_scheds) < 3:  # Skip departments with few lectures
                continue
            
            # Get all time slots used by this department
            dept_time_slots = set()
            for schedule, _ in dept_scheds:
                dept_time_slots.add(schedule.time_slot_id)
            
            # If lectures are spread across many days, try to consolidate
            if len(dept_time_slots) > 3:  # More than 3 different time slots
                # This is a simplified approach - in a real implementation,
                # we would use more sophisticated algorithms
                pass
        
        return optimized_schedules
    
    def _optimize_workload_balance(self, schedules: List[Schedule], 
                                lectures: List[Lecture]) -> List[Schedule]:
        """
        Balance workload across time slots and classrooms
        """
        # Calculate current workload distribution
        time_slot_workload = {}
        classroom_workload = {}
        
        for schedule in schedules:
            # Count lectures per time slot
            if schedule.time_slot_id not in time_slot_workload:
                time_slot_workload[schedule.time_slot_id] = 0
            time_slot_workload[schedule.time_slot_id] += 1
            
            # Count lectures per classroom
            if schedule.classroom_id not in classroom_workload:
                classroom_workload[schedule.classroom_id] = 0
            classroom_workload[schedule.classroom_id] += 1
        
        # Identify overloaded time slots and classrooms
        avg_time_slot_load = sum(time_slot_workload.values()) / len(time_slot_workload) if time_slot_workload else 0
        avg_classroom_load = sum(classroom_workload.values()) / len(classroom_workload) if classroom_workload else 0
        
        overloaded_time_slots = [
            ts_id for ts_id, load in time_slot_workload.items() 
            if load > avg_time_slot_load * 1.5
        ]
        
        overloaded_classrooms = [
            room_id for room_id, load in classroom_workload.items() 
            if load > avg_classroom_load * 1.5
        ]
        
        # Try to redistribute workload from overloaded to underloaded resources
        optimized_schedules = schedules.copy()
        
        # This is a simplified approach - in a real implementation,
        # we would use more sophisticated optimization algorithms
        # like genetic algorithms or simulated annealing
        
        return optimized_schedules
    
    def _optimize_classroom_utilization(self, schedules: List[Schedule]) -> List[Schedule]:
        """
        Optimize classroom utilization (match lecture size to room capacity)
        """
        optimized_schedules = schedules.copy()
        
        # This would involve moving lectures to more appropriately sized classrooms
        # when possible, but we need to check constraints
        
        return optimized_schedules
    
    def _optimize_daily_distribution(self, schedules: List[Schedule], 
                                  lectures: List[Lecture]) -> List[Schedule]:
        """
        Ensure even distribution of lectures across weekdays
        """
        # Group schedules by day
        day_schedules = {}
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        
        for schedule in schedules:
            time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
            if time_slot:
                day = time_slot.day
                
                if day not in day_schedules:
                    day_schedules[day] = []
                day_schedules[day].append(schedule)
        
        # Calculate average lectures per day
        total_lectures = sum(len(day_scheds) for day_scheds in day_schedules.values())
        avg_per_day = total_lectures / len(day_schedules) if day_schedules else 0
        
        # Identify overloaded days
        overloaded_days = [
            day for day, day_scheds in day_schedules.items() 
            if len(day_scheds) > avg_per_day * 1.2
        ]
        
        optimized_schedules = schedules.copy()
        
        # Try to move lectures from overloaded days to underloaded days
        # This is a simplified approach - in a real implementation,
        # we would need to check constraints and find valid alternative slots
        
        return optimized_schedules
    
    def calculate_schedule_score(self, schedules: List[Schedule], lectures: List[Lecture], 
                               groups: List[Group], departments: List[Department]) -> Dict[str, float]:
        """
        Calculate various metrics to score the quality of a schedule
        """
        scores = {
            'conflict_score': 0.0,
            'cohesion_score': 0.0,
            'balance_score': 0.0,
            'utilization_score': 0.0,
            'distribution_score': 0.0,
            'preference_score': 0.0,
            'overall_score': 0.0
        }
        
        # Check for conflicts (lower is better, so invert for scoring)
        conflicts = self.schedule_generator.get_schedule_conflicts(schedules)
        scores['conflict_score'] = max(0, 100 - len(conflicts) * 10)
        
        # Calculate departmental cohesion
        cohesion_report = self.schedule_generator.get_departmental_cohesion_report(schedules, lectures)
        avg_cohesion = sum(dept_data['cohesion_score'] for dept_data in cohesion_report.values()) / len(cohesion_report) if cohesion_report else 0
        scores['cohesion_score'] = min(100, avg_cohesion * 20)  # Scale to 100
        
        # Calculate workload balance
        time_slot_counts = {}
        for schedule in schedules:
            if schedule.time_slot_id not in time_slot_counts:
                time_slot_counts[schedule.time_slot_id] = 0
            time_slot_counts[schedule.time_slot_id] += 1
        
        if time_slot_counts:
            max_load = max(time_slot_counts.values())
            min_load = min(time_slot_counts.values())
            balance_ratio = min_load / max_load if max_load > 0 else 1
            scores['balance_score'] = balance_ratio * 100
        
        # Calculate classroom utilization efficiency
        classroom_utilization = {}
        for schedule in schedules:
            classroom = self.classroom_service.get_classroom(schedule.classroom_id)
            if classroom:
                if schedule.classroom_id not in classroom_utilization:
                    classroom_utilization[schedule.classroom_id] = []
                classroom_utilization[schedule.classroom_id].append(schedule)
        
        if classroom_utilization:
            utilization_scores = []
            for room_id, room_schedules in classroom_utilization.items():
                classroom = self.classroom_service.get_classroom(room_id)
                if classroom:
                    # Calculate utilization as percentage of capacity used
                    # This is a simplified calculation
                    utilization = len(room_schedules) / classroom.capacity * 100
                    utilization_scores.append(min(100, utilization))
            
            scores['utilization_score'] = sum(utilization_scores) / len(utilization_scores) if utilization_scores else 0
        
        # Calculate daily distribution balance
        day_counts = {}
        for schedule in schedules:
            time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
            if time_slot:
                day = time_slot.day
                if day not in day_counts:
                    day_counts[day] = 0
                day_counts[day] += 1
        
        if day_counts:
            avg_per_day = sum(day_counts.values()) / len(day_counts)
            variance = sum((count - avg_per_day) ** 2 for count in day_counts.values()) / len(day_counts)
            # Lower variance is better
            max_variance = avg_per_day ** 2  # Maximum possible variance
            distribution_score = max(0, 100 - (variance / max_variance * 100) if max_variance > 0 else 100)
            scores['distribution_score'] = distribution_score
        
        # Calculate preference satisfaction
        preference_matches = 0
        total_preferences = 0
        
        lecture_dict = {lecture.id: lecture for lecture in lectures}
        for schedule in schedules:
            if schedule.lecture_id in lecture_dict:
                lecture = lecture_dict[schedule.lecture_id]
                if lecture.time_preference:
                    total_preferences += 1
                    time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
                    if time_slot and self._matches_preference(lecture.time_preference, time_slot):
                        preference_matches += 1
        
        scores['preference_score'] = (preference_matches / total_preferences * 100) if total_preferences > 0 else 100
        
        # Calculate overall score as weighted average
        weights = {
            'conflict_score': 0.25,
            'cohesion_score': 0.15,
            'balance_score': 0.15,
            'utilization_score': 0.15,
            'distribution_score': 0.15,
            'preference_score': 0.15
        }
        
        scores['overall_score'] = sum(scores[key] * weights[key] for key in weights)
        
        return scores
    
    def _matches_preference(self, preference: str, time_slot: TimeSlot) -> bool:
        """
        Check if a time slot matches a time preference
        """
        if preference.lower() == "morning" and time_slot.id.endswith('_morning'):
            return True
        elif preference.lower() == "midday" and time_slot.id.endswith('_midday'):
            return True
        elif preference.lower() == "evening" and time_slot.id.endswith('_evening'):
            return True
        return False
    
    def iterative_optimization(self, schedules: List[Schedule], lectures: List[Lecture], 
                             groups: List[Group], departments: List[Department],
                             max_iterations: int = 100) -> List[Schedule]:
        """
        Perform iterative optimization using local search techniques
        """
        current_schedules = copy.deepcopy(schedules)
        current_score = self.calculate_schedule_score(current_schedules, lectures, groups, departments)
        
        for i in range(max_iterations):
            # Generate a neighbor solution by making small changes
            neighbor_schedules = self._generate_neighbor_solution(current_schedules)
            
            # Calculate neighbor score
            neighbor_score = self.calculate_schedule_score(neighbor_schedules, lectures, groups, departments)
            
            # If neighbor is better, accept it
            if neighbor_score['overall_score'] > current_score['overall_score']:
                current_schedules = neighbor_schedules
                current_score = neighbor_score
        
        return current_schedules
    
    def _generate_neighbor_solution(self, schedules: List[Schedule]) -> List[Schedule]:
        """
        Generate a neighbor solution by making small changes to the current schedule
        """
        # Make a copy of the schedules
        neighbor_schedules = copy.deepcopy(schedules)
        
        # If we have schedules, randomly modify one
        if neighbor_schedules:
            # Select a random schedule to modify
            idx = random.randint(0, len(neighbor_schedules) - 1)
            
            # Get available time slots and classrooms
            available_time_slots = self.time_slot_service.get_available_time_slots()
            available_classrooms = self.classroom_service.get_available_classrooms()
            
            # Randomly change either time slot or classroom
            change_type = random.choice(['time_slot', 'classroom'])
            
            if change_type == 'time_slot' and available_time_slots:
                # Change to a random available time slot
                new_time_slot = random.choice(available_time_slots)
                neighbor_schedules[idx].time_slot_id = new_time_slot.id
            elif change_type == 'classroom' and available_classrooms:
                # Change to a random available classroom
                new_classroom = random.choice(available_classrooms)
                neighbor_schedules[idx].classroom_id = new_classroom.id
        
        return neighbor_schedules