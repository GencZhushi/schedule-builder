import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('upload');

  return (
    <div className="App">
      <header className="App-header bg-primary text-white p-3 mb-4">
        <h1>Lecture Schedule Preparation System</h1>
      </header>

      <div className="container">
        {/* Navigation Tabs */}
        <ul className="nav nav-tabs mb-4">
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'upload' ? 'active' : ''}`}
              onClick={() => setActiveTab('upload')}
            >
              Upload & Parse
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'data' ? 'active' : ''}`}
              onClick={() => setActiveTab('data')}
            >
              Data Presentation
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'classroom' ? 'active' : ''}`}
              onClick={() => setActiveTab('classroom')}
            >
              Classrooms
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'timeslot' ? 'active' : ''}`}
              onClick={() => setActiveTab('timeslot')}
            >
              Time Slots
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'schedule' ? 'active' : ''}`}
              onClick={() => setActiveTab('schedule')}
            >
              Schedule
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'export' ? 'active' : ''}`}
              onClick={() => setActiveTab('export')}
            >
              Export
            </button>
          </li>
        </ul>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'upload' && <UploadTab />}
          {activeTab === 'data' && <DataPresentationTab />}
          {activeTab === 'classroom' && <ClassroomManagementTab />}
          {activeTab === 'timeslot' && <TimeSlotManagementTab />}
          {activeTab === 'schedule' && <ScheduleTab />}
          {activeTab === 'export' && <ExportTab />}
        </div>
      </div>
    </div>
  );
}

function UploadTab() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file first');
      return;
    }

    setUploadStatus('Uploading...');
    
    // In a real implementation, this would call the backend API
    setTimeout(() => {
      setUploadStatus('File uploaded and parsed successfully!');
    }, 1000);
  };

  return (
    <div>
      <h2>Upload Excel File</h2>
      <div className="mb-3">
        <label className="form-label">Select Excel File:</label>
        <input 
          type="file" 
          className="form-control" 
          onChange={handleFileChange}
          accept=".xlsx,.xls,.csv"
        />
      </div>
      <button className="btn btn-primary" onClick={handleUpload}>Upload</button>
      {uploadStatus && <div className="mt-3 alert alert-info">{uploadStatus}</div>}
      
      <div className="mt-4">
        <h4>Expected Excel Format</h4>
        <table className="table table-bordered">
          <thead>
            <tr>
              <th>Column Name</th>
              <th>Description</th>
              <th>Example Values</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Lenda_e_rreg</td>
              <td>Lecture name</td>
              <td>Mikroekonomia, Matematika për ekonomistë</td>
            </tr>
            <tr>
              <td>Dep_reale_rreg</td>
              <td>Department</td>
              <td>MK, MXH, EK, Kon, BF</td>
            </tr>
            <tr>
              <td>Sem_rreg</td>
              <td>Semester</td>
              <td>Semestri i parë (I), Semestri i tretë (III)</td>
            </tr>
            <tr>
              <td>Niveli_rreg</td>
              <td>Academic level</td>
              <td>Baçelor, Master</td>
            </tr>
            <tr>
              <td>Viti_rreg</td>
              <td>Academic year</td>
              <td>VITI I, VITI II</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

function DataPresentationTab() {
  return (
    <div>
      <h2>Data Presentation</h2>
      <p>Data visualization and analysis will be shown here after uploading and parsing an Excel file.</p>
      
      <div className="row">
        <div className="col-md-6">
          <div className="card mb-4">
            <div className="card-header">Lecture Statistics</div>
            <div className="card-body">
              <p>Charts and statistics about lectures will be displayed here.</p>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card mb-4">
            <div className="card-header">Department Analysis</div>
            <div className="card-body">
              <p>Departmental analysis and cohesion reports will be displayed here.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ClassroomManagementTab() {
  return (
    <div>
      <h2>Classroom Management</h2>
      <p>Classroom management interface will be shown here.</p>
      
      <div className="mb-3">
        <button className="btn btn-success">Add Classroom</button>
      </div>
      
      <table className="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Capacity</th>
            <th>Equipment</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>S1</td>
            <td>Room 101</td>
            <td>50</td>
            <td>Projector, Whiteboard</td>
            <td><span className="badge bg-success">Available</span></td>
            <td>
              <button className="btn btn-sm btn-primary me-1">Edit</button>
              <button className="btn btn-sm btn-danger">Delete</button>
            </td>
          </tr>
          <tr>
            <td>S2</td>
            <td>Room 102</td>
            <td>30</td>
            <td>Whiteboard</td>
            <td><span className="badge bg-success">Available</span></td>
            <td>
              <button className="btn btn-sm btn-primary me-1">Edit</button>
              <button className="btn btn-sm btn-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

function TimeSlotManagementTab() {
  return (
    <div>
      <h2>Time Slot Management</h2>
      <p>Time slot management interface will be shown here.</p>
      
      <div className="mb-3">
        <button className="btn btn-success">Add Time Slot</button>
      </div>
      
      <div className="table-responsive">
        <table className="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Day</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Duration</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>monday_morning</td>
              <td>Monday</td>
              <td>09:00</td>
              <td>11:00</td>
              <td>120 min</td>
              <td><span className="badge bg-success">Available</span></td>
              <td>
                <button className="btn btn-sm btn-primary me-1">Edit</button>
                <button className="btn btn-sm btn-danger">Delete</button>
              </td>
            </tr>
            <tr>
              <td>monday_midday</td>
              <td>Monday</td>
              <td>11:00</td>
              <td>15:00</td>
              <td>240 min</td>
              <td><span className="badge bg-success">Available</span></td>
              <td>
                <button className="btn btn-sm btn-primary me-1">Edit</button>
                <button className="btn btn-sm btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ScheduleTab() {
  return (
    <div>
      <h2>Schedule Generation</h2>
      <p>Schedule generation and optimization interface will be shown here.</p>
      
      <div className="mb-3">
        <button className="btn btn-primary">Generate Schedule</button>
        <button className="btn btn-secondary ms-2">Optimize Schedule</button>
      </div>
      
      <div className="card">
        <div className="card-header">Weekly Schedule</div>
        <div className="card-body">
          <p>Schedule visualization will be displayed here.</p>
        </div>
      </div>
    </div>
  );
}

function ExportTab() {
  return (
    <div>
      <h2>Export Schedule</h2>
      <p>Export functionality will be shown here.</p>
      
      <div className="mb-3">
        <button className="btn btn-success me-2">Export to PDF</button>
        <button className="btn btn-primary">Export to Excel</button>
      </div>
      
      <div className="alert alert-info">
        <h5>Export Options:</h5>
        <ul>
          <li>Full schedule</li>
          <li>Department-specific schedules</li>
          <li>Professor-specific schedules</li>
          <li>Group-specific schedules</li>
        </ul>
      </div>
    </div>
  );
}

export default App;