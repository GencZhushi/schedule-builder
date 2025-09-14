import API_BASE_URL from '../config/api';

class TimeSlotService {
  // Get all time slots
  async getTimeSlots() {
    try {
      const response = await fetch(`${API_BASE_URL}/timeslots`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching time slots:', error);
      throw error;
    }
  }

  // Create a new time slot
  async createTimeSlot(timeSlot) {
    try {
      const response = await fetch(`${API_BASE_URL}/timeslots`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(timeSlot),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error creating time slot:', error);
      throw error;
    }
  }

  // Update an existing time slot
  async updateTimeSlot(timeSlotId, timeSlot) {
    try {
      const response = await fetch(`${API_BASE_URL}/timeslots/${timeSlotId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(timeSlot),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error updating time slot:', error);
      throw error;
    }
  }

  // Delete a time slot
  async deleteTimeSlot(timeSlotId) {
    try {
      const response = await fetch(`${API_BASE_URL}/timeslots/${timeSlotId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error deleting time slot:', error);
      throw error;
    }
  }
}

export default new TimeSlotService();