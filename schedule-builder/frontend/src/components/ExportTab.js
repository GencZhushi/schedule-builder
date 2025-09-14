import React from 'react';

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

export default ExportTab;