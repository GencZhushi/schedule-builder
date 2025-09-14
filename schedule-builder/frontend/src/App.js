import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import UploadTab from './components/UploadTab';
import DataPresentationTab from './components/DataPresentationTab';
import ClassroomManagementTab from './components/ClassroomManagementTab';
import TimeSlotManagementTab from './components/TimeSlotManagementTab';
import ScheduleTab from './components/ScheduleTab';
import ExportTab from './components/ExportTab';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [sessionId, setSessionId] = useState(null);

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
              disabled={!sessionId}
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
          {activeTab === 'upload' && <UploadTab setSessionId={setSessionId} setActiveTab={setActiveTab} />}
          {activeTab === 'data' && <DataPresentationTab sessionId={sessionId} />}
          {activeTab === 'classroom' && <ClassroomManagementTab />}
          {activeTab === 'timeslot' && <TimeSlotManagementTab />}
          {activeTab === 'schedule' && <ScheduleTab />}
          {activeTab === 'export' && <ExportTab />}
        </div>
      </div>
    </div>
  );
}

export default App;
