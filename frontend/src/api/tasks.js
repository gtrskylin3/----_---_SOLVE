// frontend/src/api/tasks.js

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; // Adjust if your backend is on a different address

export async function fetchTasks(kes_code = null, task_type_filter = null, skip = 0, limit = 15) {
  try {
    const params = new URLSearchParams();
    if (kes_code) {
      params.append('kes_code', kes_code);
    }
    if (task_type_filter) {
      params.append('task_type_filter', task_type_filter);
    }
    params.append('skip', skip);
    params.append('limit', limit);

    const response = await fetch(`${API_BASE_URL}/tasks/?${params.toString()}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data; // Should return { tasks: [], total: 0 }
  } catch (error) {
    console.error("Error fetching tasks:", error);
    return { tasks: [], total: 0 };
  }
}

export async function checkTaskAnswer(taskId, answer) {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answer: answer }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error checking answer for task ${taskId}:`, error);
    return null;
  }
}

export async function fetchKesCodes() {
  try {
    const response = await fetch(`${API_BASE_URL}/kes-codes/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching KES codes:", error);
    return [];
  }
}
