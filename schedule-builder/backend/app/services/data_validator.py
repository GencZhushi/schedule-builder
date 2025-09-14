from typing import List, Dict, Any
from app.models.lecture import Lecture
from app.models.department import Department
from app.models.group import Group
from app.models.subgroup import Subgroup

class DataValidatorService:
    def __init__(self):
        # Define valid department codes
        self.valid_departments = ['AEM', 'EK', 'BF', 'MXH', 'Kon', 'MK']
        
        # Define valid academic levels
        self.valid_levels = ['Bachelor', 'Master', 'Baçelor']  # Including the typo from docs
        
        # Define valid academic years
        self.valid_years = ['VITI I', 'VITI II', 'VITI III']
        
        # Define valid lecture types
        self.valid_lecture_types = ['L', 'U']
        
        # Define valid course requirements
        self.valid_requirements = ['O', 'Z']
        
        # Define valid instructor types
        self.valid_instructor_types = ['P', 'A']
        
        # Define valid lecture durations
        self.valid_durations = [44, 45, 89, 90, 135]

    def validate_all_data(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate all parsed data according to business rules
        """
        lectures = parsed_data.get('lectures', [])
        departments = parsed_data.get('departments', [])
        groups = parsed_data.get('groups', [])
        subgroups = parsed_data.get('subgroups', [])
        
        errors = []
        warnings = []
        
        # Validate lectures
        lecture_errors = self.validate_lectures(lectures)
        errors.extend(lecture_errors)
        
        # Validate departments
        dept_errors, dept_warnings = self.validate_departments(departments)
        errors.extend(dept_errors)
        warnings.extend(dept_warnings)
        
        # Validate groups
        group_errors = self.validate_groups(groups)
        errors.extend(group_errors)
        
        # Validate subgroups
        subgroup_errors = self.validate_subgroups(subgroups)
        errors.extend(subgroup_errors)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def validate_lectures(self, lectures: List[Lecture]) -> List[str]:
        """
        Validate lecture data according to business rules
        """
        errors = []
        
        for lecture in lectures:
            # Validate department
            if lecture.dep_reale_rreg not in self.valid_departments:
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Invalid department code '{lecture.dep_reale_rreg}'. Valid codes are: {', '.join(self.valid_departments)}")
            
            # Validate academic level
            if lecture.niveli_rreg not in self.valid_levels:
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Invalid academic level '{lecture.niveli_rreg}'. Valid levels are: {', '.join(self.valid_levels)}")
            
            # Validate academic year
            if lecture.viti_rreg not in self.valid_years:
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Invalid academic year '{lecture.viti_rreg}'. Valid years are: {', '.join(self.valid_years)}")
            
            # Validate professor
            if not lecture.prof_rreg or lecture.prof_rreg.strip() == '':
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Missing professor name")
            
            # Validate lecture type
            if lecture.status_lende_rreg not in self.valid_lecture_types:
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Invalid lecture type '{lecture.status_lende_rreg}'. Valid types are: {', '.join(self.valid_lecture_types)} (L=Lecture, U=Exercise)")
            
            # Validate course requirement
            if lecture.qasja_lende_rreg not in self.valid_requirements:
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Invalid course requirement '{lecture.qasja_lende_rreg}'. Valid requirements are: {', '.join(self.valid_requirements)} (O=Obligatory, Z=Elective)")
            
            # Validate instructor type
            if lecture.mesimdhe_lende_rreg not in self.valid_instructor_types:
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Invalid instructor type '{lecture.mesimdhe_lende_rreg}'. Valid types are: {', '.join(self.valid_instructor_types)} (P=Professor, A=Teaching Assistant)")
            
            # Validate lecture duration
            if lecture.time_per_lec_rreg not in self.valid_durations:
                errors.append(f"Lecture '{lecture.lenda_e_rreg}': Invalid lecture duration '{lecture.time_per_lec_rreg}'. Valid durations are: {', '.join(map(str, self.valid_durations))} minutes")
        
        return errors

    def validate_departments(self, departments: List[Department]) -> tuple:
        """
        Validate department data
        """
        errors = []
        warnings = []
        
        # Check for missing departments
        parsed_dept_codes = [dept.code for dept in departments]
        for valid_dept in self.valid_departments:
            if valid_dept not in parsed_dept_codes:
                warnings.append(f"Department '{valid_dept}' not found in uploaded data")
        
        return errors, warnings

    def validate_groups(self, groups: List[Group]) -> List[str]:
        """
        Validate group data
        """
        errors = []
        
        for group in groups:
            # Validate group format
            if not group.id.startswith('Gr. '):
                errors.append(f"Invalid group format: '{group.id}'. Expected format: 'Gr. X' or 'Gr. X.Y'")
            
            # Validate daily limit
            if group.daily_limit <= 0:
                errors.append(f"Group '{group.id}': Invalid daily limit '{group.daily_limit}'")
        
        return errors

    def validate_subgroups(self, subgroups: List[Subgroup]) -> List[str]:
        """
        Validate subgroup data
        """
        errors = []
        
        for subgroup in subgroups:
            # Validate subgroup format
            if not subgroup.id.startswith('Gr. ') or '.' not in subgroup.id:
                errors.append(f"Invalid subgroup format: '{subgroup.id}'. Expected format: 'Gr. X.Y'")
            
            # Validate parent group reference
            if not subgroup.parent_group.startswith('Gr. '):
                errors.append(f"Subgroup '{subgroup.id}': Invalid parent group reference '{subgroup.parent_group}'")
            
            # Validate daily limit
            if subgroup.daily_limit <= 0:
                errors.append(f"Subgroup '{subgroup.id}': Invalid daily limit '{subgroup.daily_limit}'")
        
        return errors

    def get_data_summary(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the parsed data
        """
        lectures = parsed_data.get('lectures', [])
        departments = parsed_data.get('departments', [])
        groups = parsed_data.get('groups', [])
        subgroups = parsed_data.get('subgroups', [])
        
        # Count lectures by type
        lecture_count = sum(1 for l in lectures if l.status_lende_rreg == 'L')
        exercise_count = sum(1 for l in lectures if l.status_lende_rreg == 'U')
        
        # Count lectures by requirement
        obligatory_count = sum(1 for l in lectures if l.qasja_lende_rreg == 'O')
        elective_count = sum(1 for l in lectures if l.qasja_lende_rreg == 'Z')
        
        # Count lectures by instructor type
        professor_count = sum(1 for l in lectures if l.mesimdhe_lende_rreg == 'P')
        assistant_count = sum(1 for l in lectures if l.mesimdhe_lende_rreg == 'A')
        
        return {
            'total_lectures': len(lectures),
            'lecture_count': lecture_count,
            'exercise_count': exercise_count,
            'obligatory_count': obligatory_count,
            'elective_count': elective_count,
            'professor_count': professor_count,
            'assistant_count': assistant_count,
            'departments_count': len(departments),
            'groups_count': len(groups),
            'subgroups_count': len(subgroups)
        }