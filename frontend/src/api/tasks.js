import apiFetch from '.';

export async function fetchTasks(kes_code = null, part_filter = null, skip = 0, limit = 15) {
  const params = new URLSearchParams();
  if (kes_code) params.append('kes_code', kes_code);
  if (part_filter) params.append('part_filter', part_filter);
  params.append('skip', skip);
  params.append('limit', limit);
  return await apiFetch(`/api/v1/tasks/?${params.toString()}`);
}

export async function checkTaskAnswer(taskId, answer) {
  return await apiFetch(`/api/v1/tasks/${taskId}/check`, {
    method: 'POST',
    body: JSON.stringify({ answer: answer }),
  });
}

export async function fetchKesCodes() {
  return await apiFetch('/api/v1/kes-codes/');
}

export async function fetchDashboardStats() {
  return await apiFetch('/api/v1/me/dashboard-stats');
}

export async function fetchSolvedTasks() {
  return await apiFetch('/api/v1/me/solved-tasks');
}
