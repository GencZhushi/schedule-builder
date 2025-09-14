import React, { useState, useEffect } from 'react';
import classroomService from '../services/classroomService';

function ClassroomManagementTab() {
  const [classrooms, setClassrooms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingClassroom, setEditingClassroom] = useState(null);
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    capacity: '',
    equipment: '',
    status: 'available'
  });

  // Fetch classrooms when component mounts
  useEffect(() => {
    fetchClassrooms();
  }, []);

  const fetchClassrooms = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await classroomService.getClassrooms();
      setClassrooms(data);
    } catch (err) {
      setError('Failed to fetch classrooms: ' + err.message);
      console.error('Error fetching classrooms:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingClassroom) {
        // Update existing classroom
        await classroomService.updateClassroom(editingClassroom.id, {
          ...formData,
          capacity: parseInt(formData.capacity)
        });
        setEditingClassroom(null);
      } else {
        // Create new classroom
        await classroomService.createClassroom({
          ...formData,
          capacity: parseInt(formData.capacity)
        });
        setShowAddForm(false);
      }
      
      // Reset form
      setFormData({
        id: '',
        name: '',
        capacity: '',
        equipment: '',
        status: 'available'
      });
      
      // Refresh classroom list
      await fetchClassrooms();
    } catch (err) {
      setError('Failed to save classroom: ' + err.message);
      console.error('Error saving classroom:', err);
    }
  };

  const handleEdit = (classroom) => {
    setFormData({
      id: classroom.id,
      name: classroom.name,
      capacity: classroom.capacity.toString(),
      equipment: classroom.equipment || '',
      status: classroom.status
    });
    setEditingClassroom(classroom);
    setShowAddForm(true);
  };

  const handleDelete = async (classroomId) => {
    if (window.confirm('Are you sure you want to delete this classroom?')) {
      try {
        await classroomService.deleteClassroom(classroomId);
        await fetchClassrooms();
      } catch (err) {
        setError('Failed to delete classroom: ' + err.message);
        console.error('Error deleting classroom:', err);
      }
    }
  };

  const cancelForm = () => {
    setShowAddForm(false);
    setEditingClassroom(null);
    setFormData({
      id: '',
      name: '',
      capacity: '',
      equipment: '',
      status: 'available'
    });
  };

  if (loading && classrooms.length === 0) {
    return (
      <div className="container">
        <h2>Classroom Management</h2>
        <div className="d-flex justify-content-center mt-5">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h2>Classroom Management</h2>
      
      {error && (
        <div className="alert alert-danger alert-dismissible fade show" role="alert">
          {error}
          <button type="button" className="btn-close" onClick={() => setError(null)}></button>
        </div>
      )}
      
      <div className="mb-3">
        <button 
          className="btn btn-success" 
          onClick={() => {
            setShowAddForm(!showAddForm);
            setEditingClassroom(null);
            setFormData({
              id: '',
              name: '',
              capacity: '',
              equipment: '',
              status: 'available'
            });
          }}
        >
          {showAddForm ? 'Cancel' : 'Add Classroom'}
        </button>
      </div>
      
      {showAddForm && (
        <div className="card mb-4">
          <div className="card-header">
            <h5>{editingClassroom ? 'Edit Classroom' : 'Add New Classroom'}</h5>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">ID *</label>
                  <input
                    type="text"
                    className="form-control"
                    name="id"
                    value={formData.id}
                    onChange={handleInputChange}
                    required
                    disabled={!!editingClassroom}
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label className="form-label">Name *</label>
                  <input
                    type="text"
                    className="form-control"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
              
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">Capacity *</label>
                  <input
                    type="number"
                    className="form-control"
                    name="capacity"
                    value={formData.capacity}
                    onChange={handleInputChange}
                    min="1"
                    required
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label className="form-label">Status</label>
                  <select
                    className="form-control"
                    name="status"
                    value={formData.status}
                    onChange={handleInputChange}
                  >
                    <option value="available">Available</option>
                    <option value="unavailable">Unavailable</option>
                  </select>
                </div>
              </div>
              
              <div className="mb-3">
                <label className="form-label">Equipment</label>
                <input
                  type="text"
                  className="form-control"
                  name="equipment"
                  value={formData.equipment}
                  onChange={handleInputChange}
                  placeholder="e.g., Projector, Whiteboard, Computers"
                />
              </div>
              
              <div className="d-flex gap-2">
                <button type="submit" className="btn btn-primary">
                  {editingClassroom ? 'Update Classroom' : 'Add Classroom'}
                </button>
                <button type="button" className="btn btn-secondary" onClick={cancelForm}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      
      <div className="card">
        <div className="card-header">
          <h5>Classroom List ({classrooms.length} items)</h5>
        </div>
        <div className="card-body">
          {classrooms.length === 0 ? (
            <p className="text-muted">No classrooms found. Add a new classroom to get started.</p>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-bordered">
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
                  {classrooms.map((classroom) => (
                    <tr key={classroom.id}>
                      <td>{classroom.id}</td>
                      <td>{classroom.name}</td>
                      <td>{classroom.capacity}</td>
                      <td>{classroom.equipment || '-'}</td>
                      <td>
                        <span className={`badge ${classroom.status === 'available' ? 'bg-success' : 'bg-danger'}`}>
                          {classroom.status}
                        </span>
                      </td>
                      <td>
                        <div className="btn-group" role="group">
                          <button 
                            className="btn btn-sm btn-primary me-1" 
                            onClick={() => handleEdit(classroom)}
                          >
                            Edit
                          </button>
                          <button 
                            className="btn btn-sm btn-danger" 
                            onClick={() => handleDelete(classroom.id)}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ClassroomManagementTab;