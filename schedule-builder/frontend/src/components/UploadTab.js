import React, { useState } from 'react';
import API_BASE_URL from '../config/api';

function UploadTab({ setSessionId, setActiveTab }) {
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
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch(`${API_BASE_URL}/schedule/upload`, {
        method: 'POST',
        body: formData
      });
      
      const result = await response.json();
      
      if (response.ok) {
        setSessionId(result.session_id);
        setUploadStatus('File uploaded and parsed successfully!');
        // Automatically switch to Data Presentation tab
        setTimeout(() => setActiveTab('data'), 1000);
      } else {
        setUploadStatus(`Error: ${result.detail || 'Upload failed'}`);
      }
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    }
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
            <tr>
              <td>Prof_rreg</td>
              <td>Professor</td>
              <td>Ramiz Livoreka, Ajet Ahmeti</td>
            </tr>
            <tr>
              <td>Grup_rreg</td>
              <td>Student group</td>
              <td>Gr. 1, Gr. 2, Gr. 1.1, Gr. 1.2</td>
            </tr>
            <tr>
              <td>Status_lende_rreg</td>
              <td>Lecture type</td>
              <td>L (Lecture), U (Exercise)</td>
            </tr>
            <tr>
              <td>Qasja_lende_rreg</td>
              <td>Course requirement</td>
              <td>O (Obligatory), Z (Elective)</td>
            </tr>
            <tr>
              <td>Mesimdhe_lende_rreg</td>
              <td>Instructor type</td>
              <td>P (Professor), A (Teaching Assistant)</td>
            </tr>
            <tr>
              <td>Time_per_lec_rreg</td>
              <td>Lecture length</td>
              <td>45, 90, 135</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default UploadTab;