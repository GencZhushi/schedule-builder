import pandas as pd
from typing import List, Dict, Any
from app.models.schedule import Schedule
from app.models.lecture import Lecture
from app.models.classroom import Classroom
from app.models.time_slot import TimeSlot
from app.services.time_slot_service import TimeSlotService
import json
import os
from datetime import datetime

class ExportService:
    def __init__(self, time_slot_service: TimeSlotService):
        self.time_slot_service = time_slot_service
    
    def export_schedule_to_excel(self, schedules: List[Schedule], lectures: List[Lecture], 
                               classrooms: List[Classroom], file_path: str) -> bool:
        """
        Export schedule to Excel file
        """
        try:
            # Create a mapping for lectures
            lecture_dict = {lecture.id: lecture for lecture in lectures}
            
            # Create schedule data for export
            schedule_data = []
            for schedule in schedules:
                lecture = lecture_dict.get(schedule.lecture_id)
                classroom = next((c for c in classrooms if c.id == schedule.classroom_id), None)
                time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
                
                if lecture:
                    schedule_data.append({
                        'Lecture Name': lecture.lenda_e_rreg,
                        'Department': lecture.dep_reale_rreg,
                        'Semester': lecture.sem_rreg,
                        'Academic Level': lecture.niveli_rreg,
                        'Academic Year': lecture.viti_rreg,
                        'Professor': lecture.prof_rreg,
                        'Group': lecture.grup_rreg,
                        'Lecture Type': 'Lecture' if lecture.status_lende_rreg == 'L' else 'Exercise',
                        'Requirement': 'Obligatory' if lecture.qasja_lende_rreg == 'O' else 'Elective',
                        'Duration (min)': lecture.time_per_lec_rreg,
                        'Day': time_slot.day if time_slot else '',
                        'Start Time': time_slot.start_time if time_slot else '',
                        'End Time': time_slot.end_time if time_slot else '',
                        'Classroom': classroom.name if classroom else schedule.classroom_id,
                        'Classroom Capacity': classroom.capacity if classroom else ''
                    })
            
            # Create DataFrame and export to Excel
            df = pd.DataFrame(schedule_data)
            df.to_excel(file_path, index=False)
            
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False
    
    def export_schedule_to_pdf(self, schedules: List[Schedule], lectures: List[Lecture], 
                             classrooms: List[Classroom], file_path: str) -> bool:
        """
        Export schedule to PDF file (simplified implementation)
        """
        try:
            # For a full PDF implementation, we would use a library like reportlab
            # This is a simplified version that creates a text-based PDF representation
            
            # Create a mapping for lectures
            lecture_dict = {lecture.id: lecture for lecture in lectures}
            
            # Generate schedule table as text
            pdf_content = "LECTURE SCHEDULE\n"
            pdf_content += "=" * 50 + "\n"
            pdf_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Group schedules by day
            schedules_by_day = {}
            for schedule in schedules:
                time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
                if time_slot:
                    day = time_slot.day
                    if day not in schedules_by_day:
                        schedules_by_day[day] = []
                    schedules_by_day[day].append((schedule, time_slot))
            
            # Sort days (Monday to Friday)
            days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            
            for day in days_order:
                if day in schedules_by_day:
                    pdf_content += f"\n{day.upper()}\n"
                    pdf_content += "-" * 30 + "\n"
                    
                    # Sort by start time
                    day_schedules = sorted(schedules_by_day[day], 
                                         key=lambda x: x[1].start_time if x[1] else "")
                    
                    for schedule, time_slot in day_schedules:
                        lecture = lecture_dict.get(schedule.lecture_id)
                        classroom = next((c for c in classrooms if c.id == schedule.classroom_id), None)
                        
                        if lecture:
                            pdf_content += f"{time_slot.start_time} - {time_slot.end_time} | "
                            pdf_content += f"{lecture.lenda_e_rreg} | "
                            pdf_content += f"{lecture.prof_rreg} | "
                            pdf_content += f"{classroom.name if classroom else schedule.classroom_id}\n"
            
            # Write to file
            with open(file_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                f.write(pdf_content)
            
            return True
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            return False
    
    def export_schedule_summary(self, schedules: List[Schedule], lectures: List[Lecture], 
                              file_path: str) -> bool:
        """
        Export schedule summary to JSON
        """
        try:
            # Create a mapping for lectures
            lecture_dict = {lecture.id: lecture for lecture in lectures}
            
            # Generate summary statistics
            summary = {
                "total_lectures": len(schedules),
                "departments": {},
                "professors": {},
                "days": {},
                "generated_on": datetime.now().isoformat()
            }
            
            # Count by department
            for schedule in schedules:
                lecture = lecture_dict.get(schedule.lecture_id)
                if lecture:
                    dept = lecture.dep_reale_rreg
                    if dept not in summary["departments"]:
                        summary["departments"][dept] = 0
                    summary["departments"][dept] += 1
            
            # Count by professor
            for schedule in schedules:
                professor = schedule.professor
                if professor not in summary["professors"]:
                    summary["professors"][professor] = 0
                summary["professors"][professor] += 1
            
            # Count by day
            for schedule in schedules:
                time_slot = self.time_slot_service.get_time_slot(schedule.time_slot_id)
                if time_slot:
                    day = time_slot.day
                    if day not in summary["days"]:
                        summary["days"][day] = 0
                    summary["days"][day] += 1
            
            # Write to JSON file
            with open(file_path, 'w') as f:
                json.dump(summary, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting summary: {e}")
            return False
    
    def export_department_schedule(self, schedules: List[Schedule], lectures: List[Lecture], 
                                 department_code: str, file_path: str) -> bool:
        """
        Export schedule for a specific department
        """
        try:
            # Filter lectures by department
            dept_lectures = [l for l in lectures if l.dep_reale_rreg == department_code]
            dept_lecture_ids = {l.id for l in dept_lectures}
            
            # Filter schedules for this department
            dept_schedules = [s for s in schedules if s.lecture_id in dept_lecture_ids]
            
            # Export to Excel
            return self.export_schedule_to_excel(dept_schedules, dept_lectures, [], file_path)
        except Exception as e:
            print(f"Error exporting department schedule: {e}")
            return False
    
    def export_professor_schedule(self, schedules: List[Schedule], lectures: List[Lecture], 
                                professor_name: str, file_path: str) -> bool:
        """
        Export schedule for a specific professor
        """
        try:
            # Filter lectures by professor
            prof_lectures = [l for l in lectures if l.prof_rreg == professor_name]
            prof_lecture_ids = {l.id for l in prof_lectures}
            
            # Filter schedules for this professor
            prof_schedules = [s for s in schedules if s.lecture_id in prof_lecture_ids]
            
            # Export to Excel
            return self.export_schedule_to_excel(prof_schedules, prof_lectures, [], file_path)
        except Exception as e:
            print(f"Error exporting professor schedule: {e}")
            return False
    
    def export_group_schedule(self, schedules: List[Schedule], lectures: List[Lecture], 
                            group_id: str, file_path: str) -> bool:
        """
        Export schedule for a specific group
        """
        try:
            # Filter lectures by group
            group_lectures = [l for l in lectures if l.grup_rreg == group_id]
            group_lecture_ids = {l.id for l in group_lectures}
            
            # Filter schedules for this group
            group_schedules = [s for s in schedules if s.lecture_id in group_lecture_ids]
            
            # Export to Excel
            return self.export_schedule_to_excel(group_schedules, group_lectures, [], file_path)
        except Exception as e:
            print(f"Error exporting group schedule: {e}")
            return False