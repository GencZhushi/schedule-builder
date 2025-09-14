# Lecture Schedule Preparation System

This system automates the process of creating lecture schedules for the Faculty of Economics. It accepts Excel file uploads containing lecture data and automatically generates optimized schedules based on various constraints and requirements.

## Features

- Excel file upload and parsing
- Data validation and presentation
- Classroom management
- Time slot configuration
- Automated schedule generation with constraint checking
- Schedule optimization
- Conflict detection
- Export functionality (PDF, Excel)

## Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: React.js
- **Database**: SQLite
- **Excel Processing**: pandas, openpyxl

## Project Structure

```
schedule-builder/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── utils/        # Utility functions
│   │   ├── main.py       # Application entry point
│   │   └── config.py     # Configuration
│   ├── uploads/          # Uploaded files
│   ├── exports/          # Exported files
│   ├── requirements.txt  # Python dependencies
│   └── test_system.py    # Test suite
└── frontend/
    ├── public/           # Static files
    ├── src/
    │   ├── components/   # React components
    │   ├── pages/        # Page components
    │   ├── services/     # API service functions
    │   ├── utils/        # Utility functions
    │   ├── App.js        # Main App component
    │   ├── App.css       # App styles
    │   └── index.js      # Entry point
    ├── package.json      # Node.js dependencies
    └── README.md         # Frontend documentation
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. The backend API will be available at `http://localhost:8000`

7. Interactive API documentation is available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. The frontend will be available at `http://localhost:3000`

## API Endpoints

### File Upload and Data Management
- `POST /api/schedule/upload` - Upload and parse Excel file
- `GET /api/data/presentation/{session_id}` - Get parsed data presentation

### Classroom Management
- `GET /api/classrooms` - Get all classrooms
- `POST /api/classrooms` - Create a new classroom
- `PUT /api/classrooms/{classroom_id}` - Update a classroom
- `DELETE /api/classrooms/{classroom_id}` - Delete a classroom

### Time Slot Management
- `GET /api/timeslots` - Get all time slots
- `POST /api/timeslots` - Create a new time slot
- `PUT /api/timeslots/{time_slot_id}` - Update a time slot
- `DELETE /api/timeslots/{time_slot_id}` - Delete a time slot

### Schedule Generation and Management
- `POST /api/schedule/generate/{session_id}` - Generate schedule
- `POST /api/schedule/optimize` - Optimize current schedule
- `POST /api/schedule/save-version` - Save schedule version
- `GET /api/schedule/versions` - Get all schedule versions
- `GET /api/schedule/version/{version_id}` - Get specific schedule version

### Export Functionality
- `GET /api/export/excel` - Export schedule to Excel
- `GET /api/export/pdf` - Export schedule to PDF
- `GET /api/export/summary` - Export schedule summary to JSON

### Conflict Detection
- `GET /api/conflicts/detect` - Detect conflicts in current schedule
- `GET /api/conflicts/report` - Get detailed conflict report

### Configuration
- `GET /api/config/timeslot` - Get time slot configuration
- `PUT /api/config/timeslot` - Update time slot configuration

## Testing

Run the test suite:
```bash
cd backend
python test_system.py
```

## Expected Excel Format

The system expects Excel files with the following column structure:

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| Lenda_e_rreg | Lecture name | Mikroekonomia, Matematika për ekonomistë |
| Dep_reale_rreg | Department | MK, MXH, EK, Kon, BF |
| Sem_rreg | Semester | Semestri i parë (I), Semestri i tretë (III) |
| Niveli_rreg | Academic level | Baçelor, Master |
| Viti_rreg | Academic year | VITI I, VITI II |
| Prof_rreg | Professor | Ramiz Livoreka, Ajet Ahmeti |
| Grup_rreg | Student group | Gr. 1, Gr. 2, Gr. 1.1, Gr. 1.2 |
| Status_lende_rreg | Lecture type | L (Lecture), U (Exercise) |
| Qasja_lende_rreg | Course requirement | O (Obligatory), Z (Elective) |
| Mesimdhe_lende_rreg | Instructor type | P (Professor), A (Teaching Assistant) |
| Time_per_lec_rreg | Lecture length | 45, 90, 135 |

## License

This project is licensed under the MIT License.