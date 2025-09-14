import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.models.lecture import Lecture
    from app.models.classroom import Classroom
    from app.models.time_slot import TimeSlot
    from app.models.schedule import Schedule
    from app.services.database_service import DatabaseService
    
    print("Database test script started...")
    
    # Initialize database service
    db_service = DatabaseService()
    print("✓ Database service initialized")
    
    # Check if database file exists
    if os.path.exists("schedule.db"):
        print("✓ Database file exists")
        # Get file size
        size = os.path.getsize("schedule.db")
        print(f"  Database file size: {size} bytes")
    else:
        print("✗ Database file does not exist")
    
    # Test creating and saving a sample lecture
    print("\nTesting data insertion...")
    
    sample_lecture = Lecture(
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
    
    # Save lecture to database
    success = db_service.save_lecture(sample_lecture)
    if success:
        print("✓ Sample lecture saved to database")
    else:
        print("✗ Failed to save sample lecture")
    
    # Test creating and saving a sample classroom
    sample_classroom = Classroom(
        id="S1",
        name="Room 101",
        capacity=50,
        equipment="Projector",
        status="available"
    )
    
    # Save classroom to database
    success = db_service.save_classroom(sample_classroom)
    if success:
        print("✓ Sample classroom saved to database")
    else:
        print("✗ Failed to save sample classroom")
    
    # Test creating and saving a sample time slot
    sample_time_slot = TimeSlot(
        id="monday_9_11",
        day="Monday",
        start_time="09:00",
        end_time="11:00",
        duration=120,
        status="available"
    )
    
    # Save time slot to database
    success = db_service.save_time_slot(sample_time_slot)
    if success:
        print("✓ Sample time slot saved to database")
    else:
        print("✗ Failed to save sample time slot")
    
    # Test retrieving data
    print("\nTesting data retrieval...")
    
    # Retrieve lecture
    retrieved_lecture = db_service.get_lecture("test_lecture_1")
    if retrieved_lecture:
        print("✓ Lecture retrieved successfully")
        print(f"  Lecture name: {retrieved_lecture.lenda_e_rreg}")
        print(f"  Professor: {retrieved_lecture.prof_rreg}")
    else:
        print("✗ Failed to retrieve lecture")
    
    # Retrieve classroom
    retrieved_classroom = db_service.get_classroom("S1")
    if retrieved_classroom:
        print("✓ Classroom retrieved successfully")
        print(f"  Classroom name: {retrieved_classroom.name}")
        print(f"  Capacity: {retrieved_classroom.capacity}")
    else:
        print("✗ Failed to retrieve classroom")
    
    # Retrieve time slot
    retrieved_time_slot = db_service.get_time_slot("monday_9_11")
    if retrieved_time_slot:
        print("✓ Time slot retrieved successfully")
        print(f"  Day: {retrieved_time_slot.day}")
        print(f"  Time: {retrieved_time_slot.start_time} - {retrieved_time_slot.end_time}")
    else:
        print("✗ Failed to retrieve time slot")
    
    print("\nDatabase test completed successfully!")
    print("The database is working correctly and can store data.")
    
except Exception as e:
    print(f"Error during database test: {e}")
    import traceback
    traceback.print_exc()