# Port Configuration Fixes

## Issues Identified

1. **Inconsistent Backend Ports**:
   - [main.py](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/backend/app/main.py) specified port 8000
   - [start_server.py](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/backend/start_server.py) used port 8003
   - Startup scripts referenced port 8000

2. **Inconsistent Frontend API URLs**:
   - [classroomService.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/services/classroomService.js) used port 8006
   - [timeSlotService.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/services/timeSlotService.js) used port 8003
   - [UploadTab.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/components/UploadTab.js) used port 8006

## Fixes Applied

1. **Standardized Backend Port**:
   - Set all backend configurations to use port 8000 (standard FastAPI port)
   - Updated [start_server.py](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/backend/start_server.py) to use port 8000

2. **Centralized Frontend Configuration**:
   - Created [api.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/config/api.js) configuration file with `API_BASE_URL = 'http://localhost:8000/api'`
   - Updated all service files to import this configuration:
     - [classroomService.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/services/classroomService.js)
     - [timeSlotService.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/services/timeSlotService.js)
   - Updated [UploadTab.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/components/UploadTab.js) to use the centralized configuration

## Benefits

1. **Consistency**: All parts of the application now use the same API port (8000)
2. **Maintainability**: Future port changes only require updating one file ([api.js](file:///c:/Users/Admin/OneDrive%20-%20uni-pr.edu/Desktop/projekti_ndryshimi/schedule-builder/frontend/src/config/api.js))
3. **Reduced Errors**: Eliminates the risk of port mismatches between frontend and backend