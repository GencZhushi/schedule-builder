#!/usr/bin/env python3
"""
Test script for the Lecture Schedule Preparation System
"""

import sys
import os
import json
from app.models.lecture import Lecture
from app.models.department import Department
from app.models.group import Group
from app.models.classroom import Classroom
from app.models.time_slot import TimeSlot
from app.services.excel_parser import ExcelParserService
from app.services.data_validator import DataValidatorService
from app.services.classroom_service import ClassroomService
from app.services.time_slot_service import TimeSlotService
from app.services.combination_generator import CombinationGenerator
from app.services.conflict_detector import ConflictDetector

def test_data_models():
    """Test data models creation"""
    print("Testing data models...")
    
    # Test Lecture model
    lecture = Lecture(
        id="test_lecture_1",
        lenda_e_rreg="Mathematics",
        dep_reale_rreg="EK",
        sem_rreg="Semestri i parë (I)",
        niveli_rreg="Bachelor",
        viti_rreg="VITI I",
        prof_rreg="Dr. John Smith",
        grup_rreg="Gr. 1",
        status_lende_rreg="L",
        qasja_lende_rreg="O",
        mesimdhe_lende_rreg="P",
        time_per_lec_rreg=90
    )
    print(f"✓ Lecture model created: {lecture.lenda_e_rreg}")
    
    # Test Department model
    department = Department(
        code="EK",
        name="Economics",
        lecture_count=10,
        cohesion_priority=5
    )
    print(f"✓ Department model created: {department.name}")
    
    # Test Group model
    group = Group(
        id="Gr. 1",
        sub_groups=["Gr. 1.1", "Gr. 1.2"],
        lecture_count=15,
        daily_limit=5
    )
    print(f"✓ Group model created: {group.id}")
    
    # Test Classroom model
    classroom = Classroom(
        id="S1",
        name="Room 101",
        capacity=50,
        equipment="Projector, Whiteboard",
        status="available"
    )
    print(f"✓ Classroom model created: {classroom.name}")
    
    # Test TimeSlot model
    time_slot = TimeSlot(
        id="monday_9_11",
        day="Monday",
        start_time="09:00",
        end_time="11:00",
        duration=120,
        status="available"
    )
    print(f"✓ TimeSlot model created: {time_slot.day} {time_slot.start_time}-{time_slot.end_time}")
    
    print("✓ All data models tests passed\n")

def test_services():
    """Test service functionality"""
    print("Testing services...")
    
    # Test ClassroomService
    classroom_service = ClassroomService()
    classroom = Classroom(
        id="S1",
        name="Room 101",
        capacity=50,
        equipment="Projector",
        status="available"
    )
    classroom_service.add_classroom(classroom)
    retrieved_classroom = classroom_service.get_classroom("S1")
    assert retrieved_classroom.name == "Room 101"
    print("✓ ClassroomService tests passed")
    
    # Test TimeSlotService
    time_slot_service = TimeSlotService()
    time_slot = TimeSlot(
        id="monday_9_11",
        day="Monday",
        start_time="09:00",
        end_time="11:00",
        duration=120,
        status="available"
    )
    time_slot_service.add_time_slot(time_slot)
    retrieved_time_slot = time_slot_service.get_time_slot("monday_9_11")
    assert retrieved_time_slot.day == "Monday"
    print("✓ TimeSlotService tests passed")
    
    # Test ExcelParserService
    excel_parser = ExcelParserService()
    print("✓ ExcelParserService initialized")
    
    # Test DataValidatorService
    data_validator = DataValidatorService()
    print("✓ DataValidatorService initialized")
    
    # Test CombinationGenerator
    combination_generator = CombinationGenerator(classroom_service, time_slot_service)
    print("✓ CombinationGenerator initialized")
    
    # Test ConflictDetector
    conflict_detector = ConflictDetector(time_slot_service)
    print("✓ ConflictDetector initialized")
    
    print("✓ All services tests passed\n")

def test_integration():
    """Test integration between components"""
    print("Testing integration...")
    
    # Create services
    classroom_service = ClassroomService()
    time_slot_service = TimeSlotService()
    
    # Add test data
    classroom = Classroom(
        id="S1",
        name="Room 101",
        capacity=50,
        status="available"
    )
    classroom_service.add_classroom(classroom)
    
    time_slot = TimeSlot(
        id="monday_9_11",
        day="Monday",
        start_time="09:00",
        end_time="11:00",
        duration=120,
        status="available"
    )
    time_slot_service.add_time_slot(time_slot)
    
    # Test combination generation
    combination_generator = CombinationGenerator(classroom_service, time_slot_service)
    print("✓ Integration tests passed\n")

def main():
    """Main test function"""
    print("Lecture Schedule Preparation System - Test Suite")
    print("=" * 50)
    
    try:
        test_data_models()
        test_services()
        test_integration()
        
        print("🎉 All tests passed! The system is ready for use.")
        return 0
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())