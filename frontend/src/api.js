const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002';

const request = async (path, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed: ${response.status}`;
    try {
      const body = await response.json();
      message = body.detail || body.message || message;
    } catch {
      // Keep the generic HTTP error if the backend did not return JSON.
    }
    throw new Error(message);
  }

  return response.json();
};

export const analyzeIncident = (payload) => (
  request('/analyze', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
);

export const sendChatMessage = (payload) => (
  request('/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
);

export const getHealth = () => request('/health');

export const getMetrics = () => request('/metrics');

export const getObservability = () => request('/observability');

export { API_BASE_URL };
