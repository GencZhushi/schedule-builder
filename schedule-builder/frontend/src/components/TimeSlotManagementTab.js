import React, { useState, useEffect } from 'react';
import timeSlotService from '../services/timeSlotService';

function TimeSlotManagementTab() {
  const [timeSlots, setTimeSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingTimeSlot, setEditingTimeSlot] = useState(null);
  const [formData, setFormData] = useState({
    day: '',
    start_time: '',
    end_time: '',
    status: 'available'
  });

  useEffect(() => {
    fetchTimeSlots();
  }, []);

  const fetchTimeSlots = async () => {
    try {
      setLoading(true);
      const data = await timeSlotService.getTimeSlots();
      setTimeSlots(data);
    } catch (err) {
      setError('Failed to fetch time slots');
      console.error('Error fetching time slots:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTimeSlot = () => {
    setEditingTimeSlot(null);
    setFormData({
      day: '',
      start_time: '',
      end_time: '',
      status: 'available'
    });
    setShowModal(true);
  };

  const handleEditTimeSlot = (timeSlot) => {
    setEditingTimeSlot(timeSlot);
    setFormData({
      day: timeSlot.day,
      start_time: timeSlot.start_time,
      end_time: timeSlot.end_time,
      status: timeSlot.status
    });
    setShowModal(true);
  };

  const handleDeleteTimeSlot = async (timeSlotId) => {
    if (window.confirm('Are you sure you want to delete this time slot?')) {
      try {
        await timeSlotService.deleteTimeSlot(timeSlotId);
        fetchTimeSlots(); // Refresh the list
      } catch (err) {
        setError('Failed to delete time slot');
        console.error('Error deleting time slot:', err);
      }
    }
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const calculateDuration = (start, end) => {
    if (!start || !end) return 0;
    const [startHours, startMinutes] = start.split(':').map(Number);
    const [endHours, endMinutes] = end.split(':').map(Number);
    return (endHours * 60 + endMinutes) - (startHours * 60 + startMinutes);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const timeSlotData = {
        ...formData,
        duration: calculateDuration(formData.start_time, formData.end_time)
      };

      if (editingTimeSlot) {
        // Update existing time slot
        timeSlotData.id = editingTimeSlot.id;
        await timeSlotService.updateTimeSlot(editingTimeSlot.id, timeSlotData);
      } else {
        // Create new time slot with a unique ID
        timeSlotData.id = `${formData.day.toLowerCase()}_${Date.now()}`;
        await timeSlotService.createTimeSlot(timeSlotData);
      }

      setShowModal(false);
      fetchTimeSlots(); // Refresh the list
    } catch (err) {
      setError('Failed to save time slot');
      console.error('Error saving time slot:', err);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingTimeSlot(null);
  };

  if (loading) {
    return (
      <div>
        <h2>Time Slot Management</h2>
        <p>Loading time slots...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h2>Time Slot Management</h2>
        <p className="text-danger">{error}</p>
        <button className="btn btn-primary" onClick={fetchTimeSlots}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <h2>Time Slot Management</h2>
      
      <div className="mb-3">
        <button className="btn btn-success" onClick={handleAddTimeSlot}>Add Time Slot</button>
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
            {timeSlots && timeSlots.length > 0 ? (
              timeSlots.map((timeSlot) => (
                <tr key={timeSlot.id}>
                  <td>{timeSlot.id}</td>
                  <td>{timeSlot.day}</td>
                  <td>{timeSlot.start_time}</td>
                  <td>{timeSlot.end_time}</td>
                  <td>{timeSlot.duration} min</td>
                  <td>
                    <span className={`badge bg-${timeSlot.status === 'available' ? 'success' : 'secondary'}`}>
                      {timeSlot.status}
                    </span>
                  </td>
                  <td>
                    <button className="btn btn-sm btn-primary me-1" onClick={() => handleEditTimeSlot(timeSlot)}>Edit</button>
                    <button className="btn btn-sm btn-danger" onClick={() => handleDeleteTimeSlot(timeSlot.id)}>Delete</button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="text-center">No time slots found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Modal for adding/editing time slots */}
      {showModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">{editingTimeSlot ? 'Edit Time Slot' : 'Add Time Slot'}</h5>
                <button type="button" className="btn-close" onClick={closeModal}></button>
              </div>
              <div className="modal-body">
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label">Day</label>
                    <select 
                      className="form-select" 
                      name="day" 
                      value={formData.day} 
                      onChange={handleFormChange}
                      required
                    >
                      <option value="">Select Day</option>
                      <option value="Monday">Monday</option>
                      <option value="Tuesday">Tuesday</option>
                      <option value="Wednesday">Wednesday</option>
                      <option value="Thursday">Thursday</option>
                      <option value="Friday">Friday</option>
                    </select>
                  </div>
                  
                  <div className="mb-3">
                    <label className="form-label">Start Time</label>
                    <input 
                      type="time" 
                      className="form-control" 
                      name="start_time" 
                      value={formData.start_time} 
                      onChange={handleFormChange}
                      required
                    />
                  </div>
                  
                  <div className="mb-3">
                    <label className="form-label">End Time</label>
                    <input 
                      type="time" 
                      className="form-control" 
                      name="end_time" 
                      value={formData.end_time} 
                      onChange={handleFormChange}
                      required
                    />
                  </div>
                  
                  <div className="mb-3">
                    <label className="form-label">Status</label>
                    <select 
                      className="form-select" 
                      name="status" 
                      value={formData.status} 
                      onChange={handleFormChange}
                    >
                      <option value="available">Available</option>
                      <option value="unavailable">Unavailable</option>
                    </select>
                  </div>
                  
                  <div className="modal-footer">
                    <button type="button" className="btn btn-secondary" onClick={closeModal}>Cancel</button>
                    <button type="submit" className="btn btn-primary">Save</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default TimeSlotManagementTab;