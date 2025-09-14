from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import pandas as pd
import os
import uuid
import sqlite3
from datetime import datetime
from app.models.lecture import Lecture
from app.models.department import Department
from app.models.group import Group
from app.models.subgroup import Subgroup
from app.models.classroom import Classroom
from app.models.time_slot import TimeSlot, TimeSlotConfiguration
from app.models.schedule import Schedule
from app.services.excel_parser import ExcelParserService
from app.services.data_validator import DataValidatorService
from app.services.classroom_service import ClassroomService
from app.services.time_slot_service import TimeSlotService
from app.services.combination_generator import CombinationGenerator
from app.services.schedule_generator import ScheduleGenerator
from app.services.schedule_optimizer import ScheduleOptimizer
from app.services.data_visualization import DataVisualizationService
from app.services.database_service import DatabaseService
from app.services.export_service import ExportService
from app.services.conflict_detector import ConflictDetector

app = FastAPI(title="Lecture Schedule Preparation System", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
excel_parser = ExcelParserService()
data_validator = DataValidatorService()
classroom_service = ClassroomService()
time_slot_service = TimeSlotService()
combination_generator = CombinationGenerator(classroom_service, time_slot_service)
schedule_generator = ScheduleGenerator(classroom_service, time_slot_service)
schedule_optimizer = ScheduleOptimizer(classroom_service, time_slot_service)
data_visualization = DataVisualizationService()
database_service = DatabaseService()
export_service = ExportService(time_slot_service)
conflict_detector = ConflictDetector(time_slot_service)

# Create standard time slots on startup if none exist
if len(time_slot_service.get_all_time_slots()) == 0:
    time_slot_service.create_standard_time_slots()

# In-memory storage for parsed data
parsed_data_storage = {}
generated_schedules = []
conflicts_storage = []

@app.get("/")
def read_root():
    return {"message": "Lecture Schedule Preparation System API"}

@app.post("/api/schedule/upload")
async def upload_schedule_file(file: UploadFile = File(...)):
    """
    Upload and parse Excel file containing lecture data
    """
    try:
        # Generate unique filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="File name is missing")
        
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"uploads/{unique_filename}"
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Parse Excel file
        parse_result = excel_parser.parse_excel_file(file_path)
        
        if not parse_result["success"]:
            raise HTTPException(status_code=400, detail=parse_result["error"])
        
        # Validate parsed data
        validation_result = data_validator.validate_all_data(parse_result["data"])
        
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail={"errors": validation_result["errors"]})
        
        # Store parsed data
        session_id = str(uuid.uuid4())
        parsed_data_storage[session_id] = parse_result["data"]
        
        # Save lectures to database
        lectures = parse_result["data"].get("lectures", [])
        for lecture in lectures:
            database_service.save_lecture(lecture)
        
        # Generate data summary
        summary = data_validator.get_data_summary(parse_result["data"])
        
        return {
            "session_id": session_id,
            "message": "File uploaded and parsed successfully",
            "summary": summary,
            "validation": validation_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/presentation/{session_id}")
def get_data_presentation(session_id: str):
    """
    Get parsed data presentation for a session
    """
    if session_id not in parsed_data_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    parsed_data = parsed_data_storage[session_id]
    
    return {
        "lectures": parsed_data.get("lectures", []),
        "departments": parsed_data.get("departments", []),
        "groups": parsed_data.get("groups", []),
        "subgroups": parsed_data.get("subgroups", [])
    }

@app.get("/api/classrooms")
def get_classrooms():
    """
    Get all classrooms
    """
    classrooms = classroom_service.get_all_classrooms()
    return classrooms

@app.post("/api/classrooms")
def create_classroom(classroom: Classroom):
    """
    Create a new classroom
    """
    created_classroom = classroom_service.add_classroom(classroom)
    # Save to database
    database_service.save_classroom(classroom)
    return created_classroom

@app.put("/api/classrooms/{classroom_id}")
def update_classroom(classroom_id: str, classroom: Classroom):
    """
    Update an existing classroom
    """
    updated_classroom = classroom_service.update_classroom(classroom_id, classroom)
    if not updated_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    # Update in database
    database_service.save_classroom(classroom)
    return updated_classroom

@app.delete("/api/classrooms/{classroom_id}")
def delete_classroom(classroom_id: str):
    """
    Delete a classroom
    """
    deleted = classroom_service.delete_classroom(classroom_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return {"message": "Classroom deleted successfully"}

@app.get("/api/timeslots")
def get_time_slots():
    """
    Get all time slots
    """
    time_slots = time_slot_service.get_all_time_slots()
    return time_slots

@app.post("/api/timeslots")
def create_time_slot(time_slot: TimeSlot):
    """
    Create a new time slot
    """
    created_time_slot = time_slot_service.add_time_slot(time_slot)
    # Save to database
    database_service.save_time_slot(time_slot)
    return created_time_slot

@app.put("/api/timeslots/{time_slot_id}")
def update_time_slot(time_slot_id: str, time_slot: TimeSlot):
    """
    Update an existing time slot
    """
    updated_time_slot = time_slot_service.update_time_slot(time_slot_id, time_slot)
    if not updated_time_slot:
        raise HTTPException(status_code=404, detail="Time slot not found")
    # Update in database
    database_service.save_time_slot(time_slot)
    return updated_time_slot

@app.delete("/api/timeslots/{time_slot_id}")
def delete_time_slot(time_slot_id: str):
    """
    Delete a time slot
    """
    deleted = time_slot_service.delete_time_slot(time_slot_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Time slot not found")
    return {"message": "Time slot deleted successfully"}

# Add new API endpoints for lecture management
@app.put("/api/lectures/{lecture_id}")
def update_lecture(lecture_id: str, lecture: Lecture):
    """
    Update an existing lecture
    """
    # Update in database
    success = database_service.save_lecture(lecture)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update lecture")
    
    # Update in memory storage if it exists
    for session_id, session_data in parsed_data_storage.items():
        lectures = session_data.get("lectures", [])
        for i, existing_lecture in enumerate(lectures):
            if existing_lecture.id == lecture_id:
                lectures[i] = lecture
                break
    
    return {"message": "Lecture updated successfully", "lecture": lecture}

@app.delete("/api/lectures/{lecture_id}")
def delete_lecture(lecture_id: str):
    """
    Delete a lecture
    """
    # Delete from database
    conn = sqlite3.connect(database_service.db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lectures WHERE id = ?', (lecture_id,))
    conn.commit()
    conn.close()
    
    # Delete from memory storage if it exists
    for session_id, session_data in parsed_data_storage.items():
        lectures = session_data.get("lectures", [])
        session_data["lectures"] = [l for l in lectures if l.id != lecture_id]
    
    return {"message": "Lecture deleted successfully"}

@app.post("/api/schedule/generate/{session_id}")
def generate_schedule(session_id: str):
    """
    Generate schedule for a session
    """
    if session_id not in parsed_data_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    parsed_data = parsed_data_storage[session_id]
    lectures = parsed_data.get("lectures", [])
    groups = parsed_data.get("groups", [])
    subgroups = parsed_data.get("subgroups", [])
    
    # Generate schedule
    schedules, conflicts = schedule_generator.generate_schedule(lectures, groups, subgroups)
    
    # Store results
    generated_schedules.clear()
    generated_schedules.extend(schedules)
    conflicts_storage.clear()
    conflicts_storage.extend(conflicts)
    
    # Save schedules to database
    database_service.save_schedules(schedules)
    
    return {
        "schedules": schedules,
        "conflicts": conflicts,
        "message": f"Generated {len(schedules)} schedule items with {len(conflicts)} conflicts"
    }

@app.post("/api/schedule/optimize")
def optimize_schedule():
    """
    Optimize the current schedule
    """
    if not generated_schedules:
        raise HTTPException(status_code=400, detail="No schedule to optimize")
    
    # Get parsed data for optimization
    session_id = list(parsed_data_storage.keys())[0] if parsed_data_storage else None
    if not session_id:
        raise HTTPException(status_code=400, detail="No session data available")
    
    parsed_data = parsed_data_storage[session_id]
    lectures = parsed_data.get("lectures", [])
    groups = parsed_data.get("groups", [])
    departments = parsed_data.get("departments", [])
    
    # Optimize schedule
    optimized_schedules = schedule_optimizer.optimize_schedule(
        generated_schedules, lectures, groups, departments
    )
    
    # Update stored schedules
    generated_schedules.clear()
    generated_schedules.extend(optimized_schedules)
    
    # Save optimized schedules to database
    database_service.save_schedules(optimized_schedules)
    
    # Calculate optimization score
    score = schedule_optimizer.calculate_schedule_score(
        optimized_schedules, lectures, groups, departments
    )
    
    return {
        "schedules": optimized_schedules,
        "score": score,
        "message": "Schedule optimized successfully"
    }

@app.get("/api/schedule/dashboard/{session_id}")
def get_schedule_dashboard(session_id: str):
    """
    Get dashboard data for schedule visualization
    """
    if session_id not in parsed_data_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    parsed_data = parsed_data_storage[session_id]
    
    # Generate dashboard data
    dashboard_data = data_visualization.generate_summary_dashboard(
        parsed_data, generated_schedules, conflicts_storage, time_slot_service
    )
    
    return dashboard_data

@app.post("/api/schedule/save-version")
def save_schedule_version(version_name: Optional[str] = None):
    """
    Save current schedule as a version
    """
    if not generated_schedules:
        raise HTTPException(status_code=400, detail="No schedule to save")
    
    # Save to database
    success = database_service.save_schedule_version(generated_schedules, version_name or "")
    
    if success:
        return {"message": "Schedule version saved successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to save schedule version")

@app.get("/api/schedule/versions")
def get_schedule_versions():
    """
    Get all saved schedule versions
    """
    versions = database_service.get_schedule_versions()
    return versions

@app.get("/api/schedule/version/{version_id}")
def get_schedule_version(version_id: int):
    """
    Get a specific schedule version
    """
    schedules = database_service.get_schedule_version(version_id)
    if schedules is None:
        raise HTTPException(status_code=404, detail="Schedule version not found")
    return schedules

@app.get("/api/export/excel")
def export_schedule_excel():
    """
    Export current schedule to Excel
    """
    if not generated_schedules:
        raise HTTPException(status_code=400, detail="No schedule to export")
    
    # Get parsed data for export
    session_id = list(parsed_data_storage.keys())[0] if parsed_data_storage else None
    if not session_id:
        raise HTTPException(status_code=400, detail="No session data available")
    
    parsed_data = parsed_data_storage[session_id]
    lectures = parsed_data.get("lectures", [])
    classrooms = classroom_service.get_all_classrooms()
    
    # Generate filename
    filename = f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = f"exports/{filename}"
    
    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)
    
    # Export to Excel
    success = export_service.export_schedule_to_excel(generated_schedules, lectures, classrooms, file_path)
    
    if success:
        return FileResponse(file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        raise HTTPException(status_code=500, detail="Failed to export schedule")

@app.get("/api/export/pdf")
def export_schedule_pdf():
    """
    Export current schedule to PDF
    """
    if not generated_schedules:
        raise HTTPException(status_code=400, detail="No schedule to export")
    
    # Get parsed data for export
    session_id = list(parsed_data_storage.keys())[0] if parsed_data_storage else None
    if not session_id:
        raise HTTPException(status_code=400, detail="No session data available")
    
    parsed_data = parsed_data_storage[session_id]
    lectures = parsed_data.get("lectures", [])
    classrooms = classroom_service.get_all_classrooms()
    
    # Generate filename
    filename = f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = f"exports/{filename}"
    
    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)
    
    # Export to PDF (simplified as text file)
    success = export_service.export_schedule_to_pdf(generated_schedules, lectures, classrooms, file_path)
    
    if success:
        txt_file_path = file_path.replace('.pdf', '.txt')
        return FileResponse(txt_file_path, filename=filename.replace('.pdf', '.txt'), media_type='text/plain')
    else:
        raise HTTPException(status_code=500, detail="Failed to export schedule")

@app.get("/api/export/summary")
def export_schedule_summary():
    """
    Export schedule summary to JSON
    """
    if not generated_schedules:
        raise HTTPException(status_code=400, detail="No schedule to export")
    
    # Get parsed data for export
    session_id = list(parsed_data_storage.keys())[0] if parsed_data_storage else None
    if not session_id:
        raise HTTPException(status_code=400, detail="No session data available")
    
    parsed_data = parsed_data_storage[session_id]
    lectures = parsed_data.get("lectures", [])
    
    # Generate filename
    filename = f"schedule_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = f"exports/{filename}"
    
    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)
    
    # Export summary
    success = export_service.export_schedule_summary(generated_schedules, lectures, file_path)
    
    if success:
        return FileResponse(file_path, filename=filename, media_type='application/json')
    else:
        raise HTTPException(status_code=500, detail="Failed to export schedule summary")

@app.get("/api/conflicts/detect")
def detect_conflicts():
    """
    Detect conflicts in the current schedule
    """
    if not generated_schedules:
        raise HTTPException(status_code=400, detail="No schedule to analyze")
    
    # Get parsed data for conflict detection
    session_id = list(parsed_data_storage.keys())[0] if parsed_data_storage else None
    if not session_id:
        raise HTTPException(status_code=400, detail="No session data available")
    
    parsed_data = parsed_data_storage[session_id]
    lectures = parsed_data.get("lectures", [])
    
    # Detect conflicts
    conflicts = conflict_detector.detect_all_conflicts(generated_schedules, lectures)
    
    # Generate report
    report = conflict_detector.generate_conflict_report(conflicts)
    
    return report

@app.get("/api/conflicts/report")
def get_conflict_report():
    """
    Get detailed conflict report
    """
    if not generated_schedules:
        raise HTTPException(status_code=400, detail="No schedule to analyze")
    
    # Get parsed data for conflict detection
    session_id = list(parsed_data_storage.keys())[0] if parsed_data_storage else None
    if not session_id:
        raise HTTPException(status_code=400, detail="No session data available")
    
    parsed_data = parsed_data_storage[session_id]
    lectures = parsed_data.get("lectures", [])
    
    # Detect conflicts
    conflicts = conflict_detector.detect_all_conflicts(generated_schedules, lectures)
    
    # Generate detailed report
    report = conflict_detector.generate_conflict_report(conflicts)
    
    return report

@app.get("/api/config/timeslot")
def get_time_slot_configuration():
    """
    Get time slot configuration
    """
    config = time_slot_service.get_configuration()
    return config

@app.put("/api/config/timeslot")
def update_time_slot_configuration(config: TimeSlotConfiguration):
    """
    Update time slot configuration
    """
    updated_config = time_slot_service.update_configuration(config)
    return updated_config

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)