import sqlite3
import json
from typing import List, Optional, Dict, Any
from app.models.schedule import Schedule
from app.models.lecture import Lecture
from app.models.classroom import Classroom
from app.models.time_slot import TimeSlot
from datetime import datetime
import os

class DatabaseService:
    def __init__(self, db_path: str = "schedule.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        Initialize the database with required tables
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create schedules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id TEXT PRIMARY KEY,
                lecture_id TEXT NOT NULL,
                time_slot_id TEXT NOT NULL,
                classroom_id TEXT NOT NULL,
                professor TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create lectures table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lectures (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create classrooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classrooms (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create time_slots table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_slots (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create schedule_versions table for versioning
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_data TEXT NOT NULL,
                version_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_schedule(self, schedule: Schedule) -> bool:
        """
        Save a schedule to the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO schedules 
                (id, lecture_id, time_slot_id, classroom_id, professor, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                schedule.id,
                schedule.lecture_id,
                schedule.time_slot_id,
                schedule.classroom_id,
                schedule.professor,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving schedule: {e}")
            return False
    
    def save_schedules(self, schedules: List[Schedule]) -> bool:
        """
        Save multiple schedules to the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for schedule in schedules:
                cursor.execute('''
                    INSERT OR REPLACE INTO schedules 
                    (id, lecture_id, time_slot_id, classroom_id, professor, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    schedule.id,
                    schedule.lecture_id,
                    schedule.time_slot_id,
                    schedule.classroom_id,
                    schedule.professor,
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving schedules: {e}")
            return False
    
    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        """
        Retrieve a schedule by ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM schedules WHERE id = ?', (schedule_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return Schedule(
                    id=row[0],
                    lecture_id=row[1],
                    time_slot_id=row[2],
                    classroom_id=row[3],
                    professor=row[4],
                    created_at=datetime.fromisoformat(row[5]) if row[5] else None,
                    updated_at=datetime.fromisoformat(row[6]) if row[6] else None
                )
            return None
        except Exception as e:
            print(f"Error retrieving schedule: {e}")
            return None
    
    def get_all_schedules(self) -> List[Schedule]:
        """
        Retrieve all schedules
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM schedules ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            schedules = []
            for row in rows:
                schedule = Schedule(
                    id=row[0],
                    lecture_id=row[1],
                    time_slot_id=row[2],
                    classroom_id=row[3],
                    professor=row[4],
                    created_at=datetime.fromisoformat(row[5]) if row[5] else None,
                    updated_at=datetime.fromisoformat(row[6]) if row[6] else None
                )
                schedules.append(schedule)
            
            return schedules
        except Exception as e:
            print(f"Error retrieving schedules: {e}")
            return []
    
    def delete_schedule(self, schedule_id: str) -> bool:
        """
        Delete a schedule by ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM schedules WHERE id = ?', (schedule_id,))
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting schedule: {e}")
            return False
    
    def save_lecture(self, lecture: Lecture) -> bool:
        """
        Save a lecture to the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            lecture_data = json.dumps(lecture.dict())
            
            cursor.execute('''
                INSERT OR REPLACE INTO lectures (id, data)
                VALUES (?, ?)
            ''', (lecture.id, lecture_data))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving lecture: {e}")
            return False
    
    def get_lecture(self, lecture_id: str) -> Optional[Lecture]:
        """
        Retrieve a lecture by ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT data FROM lectures WHERE id = ?', (lecture_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                lecture_data = json.loads(row[0])
                return Lecture(**lecture_data)
            return None
        except Exception as e:
            print(f"Error retrieving lecture: {e}")
            return None
    
    def save_classroom(self, classroom: Classroom) -> bool:
        """
        Save a classroom to the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            classroom_data = json.dumps(classroom.dict())
            
            cursor.execute('''
                INSERT OR REPLACE INTO classrooms (id, data)
                VALUES (?, ?)
            ''', (classroom.id, classroom_data))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving classroom: {e}")
            return False
    
    def get_classroom(self, classroom_id: str) -> Optional[Classroom]:
        """
        Retrieve a classroom by ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT data FROM classrooms WHERE id = ?', (classroom_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                classroom_data = json.loads(row[0])
                return Classroom(**classroom_data)
            return None
        except Exception as e:
            print(f"Error retrieving classroom: {e}")
            return None
    
    def save_time_slot(self, time_slot: TimeSlot) -> bool:
        """
        Save a time slot to the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            time_slot_data = json.dumps(time_slot.dict())
            
            cursor.execute('''
                INSERT OR REPLACE INTO time_slots (id, data)
                VALUES (?, ?)
            ''', (time_slot.id, time_slot_data))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving time slot: {e}")
            return False
    
    def get_time_slot(self, time_slot_id: str) -> Optional[TimeSlot]:
        """
        Retrieve a time slot by ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT data FROM time_slots WHERE id = ?', (time_slot_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                time_slot_data = json.loads(row[0])
                return TimeSlot(**time_slot_data)
            return None
        except Exception as e:
            print(f"Error retrieving time slot: {e}")
            return None
    
    def save_schedule_version(self, schedules: List[Schedule], version_name: str = None) -> bool:
        """
        Save a version of the schedule
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            schedule_data = json.dumps([schedule.dict() for schedule in schedules])
            
            cursor.execute('''
                INSERT INTO schedule_versions (schedule_data, version_name)
                VALUES (?, ?)
            ''', (schedule_data, version_name))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving schedule version: {e}")
            return False
    
    def get_schedule_versions(self) -> List[Dict[str, Any]]:
        """
        Retrieve all schedule versions
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, version_name, created_at FROM schedule_versions ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            versions = []
            for row in rows:
                versions.append({
                    'id': row[0],
                    'version_name': row[1],
                    'created_at': row[2]
                })
            
            return versions
        except Exception as e:
            print(f"Error retrieving schedule versions: {e}")
            return []
    
    def get_schedule_version(self, version_id: int) -> Optional[List[Schedule]]:
        """
        Retrieve a specific schedule version
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT schedule_data FROM schedule_versions WHERE id = ?', (version_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                schedule_data = json.loads(row[0])
                return [Schedule(**data) for data in schedule_data]
            return None
        except Exception as e:
            print(f"Error retrieving schedule version: {e}")
            return None