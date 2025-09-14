import React, { useState, useEffect } from 'react';

function DataPresentationTab({ sessionId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [editingLecture, setEditingLecture] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [graphs, setGraphs] = useState({});

  useEffect(() => {
    if (sessionId) {
      fetchData();
    }
  }, [sessionId]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8006/api/data/presentation/${sessionId}`);
      
      if (response.ok) {
        const result = await response.json();
        setData(result);
        generateGraphs(result);
      } else {
        setError('Failed to fetch data');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const generateGraphs = (data) => {
    if (!data || !data.lectures) return;

    // Department distribution
    const deptCounts = {};
    data.lectures.forEach(lecture => {
      deptCounts[lecture.dep_reale_rreg] = (deptCounts[lecture.dep_reale_rreg] || 0) + 1;
    });

    // Lecture type distribution
    const typeCounts = {
      'Lecture': data.lectures.filter(l => l.status_lende_rreg === 'L').length,
      'Exercise': data.lectures.filter(l => l.status_lende_rreg === 'U').length
    };

    // Requirement distribution
    const reqCounts = {
      'Obligatory': data.lectures.filter(l => l.qasja_lende_rreg === 'O').length,
      'Elective': data.lectures.filter(l => l.qasja_lende_rreg === 'Z').length
    };

    // Duration distribution
    const durationCounts = {};
    data.lectures.forEach(lecture => {
      const duration = lecture.time_per_lec_rreg;
      durationCounts[duration] = (durationCounts[duration] || 0) + 1;
    });

    setGraphs({
      departments: deptCounts,
      types: typeCounts,
      requirements: reqCounts,
      durations: durationCounts
    });
  };

  const startEditing = (lecture) => {
    setEditingLecture(lecture.id);
    setEditForm({...lecture});
  };

  const cancelEditing = () => {
    setEditingLecture(null);
    setEditForm({});
  };

  const saveEdit = async () => {
    try {
      const response = await fetch(`http://localhost:8006/api/lectures/${editForm.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editForm)
      });

      if (response.ok) {
        // Update local data
        const updatedLectures = data.lectures.map(lecture => 
          lecture.id === editForm.id ? editForm : lecture
        );
        setData({...data, lectures: updatedLectures});
        setEditingLecture(null);
        setEditForm({});
      } else {
        alert('Failed to update lecture');
      }
    } catch (error) {
      console.error('Error updating lecture:', error);
      alert('Error updating lecture');
    }
  };

  const handleInputChange = (field, value) => {
    setEditForm({
      ...editForm,
      [field]: value
    });
  };

  const renderGraph = (title, data, type = 'bar') => {
    if (!data) return null;

    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Find the maximum value for scaling
    const maxValue = Math.max(...values, 1);
    
    // Define a maximum height for the bars
    const maxBarHeight = 150;

    return (
      <div className="card mb-4">
        <div className="card-header">
          <h5>{title}</h5>
        </div>
        <div className="card-body">
          <div className="graph-container">
            {labels.map((label, index) => {
              // Calculate height as a percentage of the maximum value
              const barHeight = (values[index] / maxValue) * maxBarHeight;
              return (
                <div key={label} className="graph-bar" style={{marginRight: '10px', display: 'inline-block', textAlign: 'center'}}>
                  <div 
                    className="bar-fill bg-primary" 
                    style={{width: '50px', height: `${barHeight}px`, marginBottom: '5px'}}
                  ></div>
                  <div className="bar-label">{label}</div>
                  <div className="bar-value">{values[index]}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center mt-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        {error}
      </div>
    );
  }

  if (!data) {
    return (
      <div>
        <h2>Data Presentation</h2>
        <p>No data available. Please upload and parse an Excel file first.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Data Presentation</h2>
      <p>All extracted data from your Excel file is displayed below:</p>
      
      {/* Graphs Section */}
      <div className="mb-4">
        <h4>Data Visualization</h4>
        {renderGraph('Lectures by Department', graphs.departments)}
        {renderGraph('Lecture Types', graphs.types, 'pie')}
        {renderGraph('Course Requirements', graphs.requirements, 'pie')}
        {renderGraph('Lecture Durations (minutes)', graphs.durations)}
      </div>
      
      {/* Lectures Table */}
      <div className="card mb-4">
        <div className="card-header">
          <h5>Lectures ({data.lectures.length} items)</h5>
        </div>
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-striped table-bordered">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Lecture Name</th>
                  <th>Department</th>
                  <th>Semester</th>
                  <th>Level</th>
                  <th>Year</th>
                  <th>Professor</th>
                  <th>Group</th>
                  <th>Type</th>
                  <th>Requirement</th>
                  <th>Instructor</th>
                  <th>Duration</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.lectures.map((lecture, index) => (
                  <tr key={lecture.id || index}>
                    {editingLecture === lecture.id ? (
                      <>
                        <td>{lecture.id || index + 1}</td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control" 
                            value={editForm.lenda_e_rreg || ''} 
                            onChange={(e) => handleInputChange('lenda_e_rreg', e.target.value)}
                          />
                        </td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control" 
                            value={editForm.dep_reale_rreg || ''} 
                            onChange={(e) => handleInputChange('dep_reale_rreg', e.target.value)}
                          />
                        </td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control" 
                            value={editForm.sem_rreg || ''} 
                            onChange={(e) => handleInputChange('sem_rreg', e.target.value)}
                          />
                        </td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control" 
                            value={editForm.niveli_rreg || ''} 
                            onChange={(e) => handleInputChange('niveli_rreg', e.target.value)}
                          />
                        </td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control" 
                            value={editForm.viti_rreg || ''} 
                            onChange={(e) => handleInputChange('viti_rreg', e.target.value)}
                          />
                        </td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control" 
                            value={editForm.prof_rreg || ''} 
                            onChange={(e) => handleInputChange('prof_rreg', e.target.value)}
                          />
                        </td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control" 
                            value={editForm.grup_rreg || ''} 
                            onChange={(e) => handleInputChange('grup_rreg', e.target.value)}
                          />
                        </td>
                        <td>
                          <select 
                            className="form-control" 
                            value={editForm.status_lende_rreg || ''} 
                            onChange={(e) => handleInputChange('status_lende_rreg', e.target.value)}
                          >
                            <option value="L">Lecture</option>
                            <option value="U">Exercise</option>
                          </select>
                        </td>
                        <td>
                          <select 
                            className="form-control" 
                            value={editForm.qasja_lende_rreg || ''} 
                            onChange={(e) => handleInputChange('qasja_lende_rreg', e.target.value)}
                          >
                            <option value="O">Obligatory</option>
                            <option value="Z">Elective</option>
                          </select>
                        </td>
                        <td>
                          <select 
                            className="form-control" 
                            value={editForm.mesimdhe_lende_rreg || ''} 
                            onChange={(e) => handleInputChange('mesimdhe_lende_rreg', e.target.value)}
                          >
                            <option value="P">Professor</option>
                            <option value="A">Assistant</option>
                          </select>
                        </td>
                        <td>
                          <input 
                            type="number" 
                            className="form-control" 
                            value={editForm.time_per_lec_rreg || ''} 
                            onChange={(e) => handleInputChange('time_per_lec_rreg', parseInt(e.target.value))}
                          />
                        </td>
                        <td>
                          <button className="btn btn-sm btn-success me-1" onClick={saveEdit}>Save</button>
                          <button className="btn btn-sm btn-secondary" onClick={cancelEditing}>Cancel</button>
                        </td>
                      </>
                    ) : (
                      <>
                        <td>{lecture.id || index + 1}</td>
                        <td>{lecture.lenda_e_rreg}</td>
                        <td>{lecture.dep_reale_rreg}</td>
                        <td>{lecture.sem_rreg}</td>
                        <td>{lecture.niveli_rreg}</td>
                        <td>{lecture.viti_rreg}</td>
                        <td>{lecture.prof_rreg}</td>
                        <td>{lecture.grup_rreg}</td>
                        <td>{lecture.status_lende_rreg}</td>
                        <td>{lecture.qasja_lende_rreg}</td>
                        <td>{lecture.mesimdhe_lende_rreg}</td>
                        <td>{lecture.time_per_lec_rreg} min</td>
                        <td>
                          <button className="btn btn-sm btn-primary" onClick={() => startEditing(lecture)}>Edit</button>
                        </td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      {/* Departments Table */}
      <div className="card mb-4">
        <div className="card-header">
          <h5>Departments ({data.departments.length} items)</h5>
        </div>
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-striped table-bordered">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Lecture Count</th>
                </tr>
              </thead>
              <tbody>
                {data.departments.map((dept, index) => (
                  <tr key={dept.code || index}>
                    <td>{dept.code}</td>
                    <td>{dept.name}</td>
                    <td>{dept.lecture_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      {/* Groups Table */}
      <div className="card mb-4">
        <div className="card-header">
          <h5>Groups ({data.groups.length} items)</h5>
        </div>
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-striped table-bordered">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Subgroups</th>
                  <th>Lecture Count</th>
                </tr>
              </thead>
              <tbody>
                {data.groups.map((group, index) => (
                  <tr key={group.id || index}>
                    <td>{group.id}</td>
                    <td>{group.sub_groups.join(', ') || 'None'}</td>
                    <td>{group.lecture_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      {/* Subgroups Table */}
      <div className="card mb-4">
        <div className="card-header">
          <h5>Subgroups ({data.subgroups.length} items)</h5>
        </div>
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-striped table-bordered">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Parent Group</th>
                  <th>Lecture Count</th>
                </tr>
              </thead>
              <tbody>
                {data.subgroups.map((subgroup, index) => (
                  <tr key={subgroup.id || index}>
                    <td>{subgroup.id}</td>
                    <td>{subgroup.parent_group}</td>
                    <td>{subgroup.lecture_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataPresentationTab;