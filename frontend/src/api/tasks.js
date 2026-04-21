// frontend/src/api/tasks.js

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; // Adjust if your backend is on a different address

export async function fetchTasks() {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching tasks:", error);
    return [];
  }
}
