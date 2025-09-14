import pandas as pd
from typing import List, Dict, Any
from app.models.lecture import Lecture
from app.models.department import Department
from app.models.group import Group
from app.models.subgroup import Subgroup

class ExcelParserService:
    def __init__(self):
        # Define expected columns based on the documentation
        self.expected_columns = [
            'Lenda_e_rreg', 'Dep_reale_rreg', 'Sem_rreg', 'Niveli_rreg', 
            'Viti_rreg', 'Prof_rreg', 'Grup_rreg', 'Status_lende_rreg', 
            'Qasja_lende_rreg', 'Mesimdhe_lende_rreg', 'Time_per_lec_rreg'
        ]
        
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

    def parse_excel_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse Excel file and extract lecture data
        """
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate columns
            validation_result = self.validate_columns(df)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': f"Column validation failed: {validation_result['message']}",
                    'data': None
                }
            
            # Parse data
            lectures = self.parse_lectures(df)
            departments = self.parse_departments(df)
            groups = self.parse_groups(df)
            subgroups = self.parse_subgroups(df)
            
            return {
                'success': True,
                'error': None,
                'data': {
                    'lectures': lectures,
                    'departments': departments,
                    'groups': groups,
                    'subgroups': subgroups
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error parsing Excel file: {str(e)}",
                'data': None
            }

    def validate_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate that the Excel file has the expected columns
        """
        missing_columns = [col for col in self.expected_columns if col not in df.columns]
        
        if missing_columns:
            return {
                'valid': False,
                'message': f"Missing columns: {', '.join(missing_columns)}"
            }
        
        return {
            'valid': True,
            'message': "All required columns present"
        }

    def parse_lectures(self, df: pd.DataFrame) -> List[Lecture]:
        """
        Parse lecture data from DataFrame
        """
        lectures = []
        
        for index, row in df.iterrows():
            # Create unique ID for the lecture
            lecture_id = f"lec_{index}"
            
            lecture = Lecture(
                id=lecture_id,
                lenda_e_rreg=str(row['Lenda_e_rreg']),
                dep_reale_rreg=str(row['Dep_reale_rreg']),
                sem_rreg=str(row['Sem_rreg']),
                niveli_rreg=str(row['Niveli_rreg']),
                viti_rreg=str(row['Viti_rreg']),
                prof_rreg=str(row['Prof_rreg']),
                grup_rreg=str(row['Grup_rreg']),
                status_lende_rreg=str(row['Status_lende_rreg']),
                qasja_lende_rreg=str(row['Qasja_lende_rreg']),
                mesimdhe_lende_rreg=str(row['Mesimdhe_lende_rreg']),
                time_per_lec_rreg=int(row['Time_per_lec_rreg'])
            )
            
            lectures.append(lecture)
        
        return lectures

    def parse_departments(self, df: pd.DataFrame) -> List[Department]:
        """
        Parse department data from DataFrame
        """
        departments = {}
        
        for _, row in df.iterrows():
            dept_code = row['Dep_reale_rreg']
            
            # Skip if department already processed
            if dept_code in departments:
                departments[dept_code].lecture_count += 1
                continue
            
            # Map department codes to full names
            dept_names = {
                'AEM': 'Applied Economics and Management',
                'EK': 'Economics',
                'BF': 'Business Finance',
                'MXH': 'Management and Human Resources',
                'Kon': 'Accounting'
            }
            
            department = Department(
                code=dept_code,
                name=dept_names.get(dept_code, dept_code),
                lecture_count=1
            )
            
            departments[dept_code] = department
        
        return list(departments.values())

    def parse_groups(self, df: pd.DataFrame) -> List[Group]:
        """
        Parse group data from DataFrame
        """
        groups = {}
        
        for _, row in df.iterrows():
            group_id = row['Grup_rreg']
            
            # Extract main group (e.g., "Gr. 1" from "Gr. 1.1")
            main_group = group_id.split('.')[0] + '.' + group_id.split('.')[1] if '.' in group_id else group_id
            
            # Skip if group already processed
            if main_group in groups:
                groups[main_group].lecture_count += 1
                # Add subgroup if it exists
                if '.' in group_id and group_id not in groups[main_group].sub_groups:
                    groups[main_group].sub_groups.append(group_id)
                continue
            
            # Create new group
            group = Group(
                id=main_group,
                sub_groups=[group_id] if '.' in group_id else [],
                lecture_count=1
            )
            
            groups[main_group] = group
        
        return list(groups.values())

    def parse_subgroups(self, df: pd.DataFrame) -> List[Subgroup]:
        """
        Parse subgroup data from DataFrame
        """
        subgroups = {}
        
        for _, row in df.iterrows():
            group_id = row['Grup_rreg']
            
            # Only process subgroups (entries with dot notation like "Gr. 1.1")
            if '.' not in group_id:
                continue
                
            # Skip if subgroup already processed
            if group_id in subgroups:
                subgroups[group_id].lecture_count += 1
                continue
            
            # Extract parent group (e.g., "Gr. 1" from "Gr. 1.1")
            parent_group = '.'.join(group_id.split('.')[:2])
            
            # Create new subgroup
            subgroup = Subgroup(
                id=group_id,
                parent_group=parent_group,
                lecture_count=1
            )
            
            subgroups[group_id] = subgroup
        
        return list(subgroups.values())

    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate parsed data according to business rules
        """
        lectures = data.get('lectures', [])
        departments = data.get('departments', [])
        groups = data.get('groups', [])
        
        errors = []
        
        # Validate lectures
        for lecture in lectures:
            # Validate department
            if lecture.dep_reale_rreg not in self.valid_departments:
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Invalid department code '{lecture.dep_reale_rreg}'")
            
            # Validate academic level
            if lecture.niveli_rreg not in self.valid_levels:
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Invalid academic level '{lecture.niveli_rreg}'")
            
            # Validate academic year
            if lecture.viti_rreg not in self.valid_years:
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Invalid academic year '{lecture.viti_rreg}'")
            
            # Validate professor
            if not lecture.prof_rreg or lecture.prof_rreg.strip() == '':
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Missing professor name")
            
            # Validate lecture type
            if lecture.status_lende_rreg not in self.valid_lecture_types:
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Invalid lecture type '{lecture.status_lende_rreg}'")
            
            # Validate course requirement
            if lecture.qasja_lende_rreg not in self.valid_requirements:
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Invalid course requirement '{lecture.qasja_lende_rreg}'")
            
            # Validate instructor type
            if lecture.mesimdhe_lende_rreg not in self.valid_instructor_types:
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Invalid instructor type '{lecture.mesimdhe_lende_rreg}'")
            
            # Validate lecture duration
            if lecture.time_per_lec_rreg not in self.valid_durations:
                errors.append(f"Lecture {lecture.lenda_e_rreg}: Invalid lecture duration '{lecture.time_per_lec_rreg}'")
        
        # Validate departments
        dept_codes = [dept.code for dept in departments]
        for dept_code in self.valid_departments:
            if dept_code not in dept_codes:
                # This is just a warning, not an error
                pass
        
        # Validate groups format
        for group in groups:
            if not group.id.startswith('Gr. '):
                errors.append(f"Invalid group format: '{group.id}'")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }