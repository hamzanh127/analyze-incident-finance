const API_BASE_URL = 'http://localhost:8002';

export const analyzeIncident = async (payload) => {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('Failed to analyze incident');
  }

  return response.json();
};

export const getHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('Failed to get health status');
  }
  return response.json();
};

export const getMetrics = async () => {
  const response = await fetch(`${API_BASE_URL}/metrics`);
  if (!response.ok) {
    throw new Error('Failed to get metrics');
  }
  return response.json();
};
