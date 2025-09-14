import API_BASE_URL from '../config/api';

class ClassroomService {
  // Get all classrooms
  async getClassrooms() {
    try {
      const response = await fetch(`${API_BASE_URL}/classrooms`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching classrooms:', error);
      throw error;
    }
  }

  // Create a new classroom
  async createClassroom(classroom) {
    try {
      const response = await fetch(`${API_BASE_URL}/classrooms`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(classroom),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error creating classroom:', error);
      throw error;
    }
  }

  // Update an existing classroom
  async updateClassroom(classroomId, classroom) {
    try {
      const response = await fetch(`${API_BASE_URL}/classrooms/${classroomId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(classroom),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error updating classroom:', error);
      throw error;
    }
  }

  // Delete a classroom
  async deleteClassroom(classroomId) {
    try {
      const response = await fetch(`${API_BASE_URL}/classrooms/${classroomId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error deleting classroom:', error);
      throw error;
    }
  }
}

export default new ClassroomService();