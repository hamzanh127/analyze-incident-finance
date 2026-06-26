const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002';

let capabilityCache = null;

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

const getApiCapabilities = async () => {
  if (capabilityCache) return capabilityCache;

  try {
    const schema = await request('/openapi.json');
    capabilityCache = {
      paths: schema?.paths || {},
      hasObservability: Boolean(schema?.paths?.['/observability']),
      hasChat: Boolean(schema?.paths?.['/chat']),
    };
  } catch {
    capabilityCache = {
      paths: {},
      hasObservability: false,
      hasChat: false,
    };
  }

  return capabilityCache;
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

export const getObservability = async () => {
  const capabilities = await getApiCapabilities();
  if (!capabilities.hasObservability) {
    return {
      langsmith_enabled: false,
      tracing: false,
      project: 'finance-incident-multi-agent',
      environment: 'unknown',
      version: 'N/A',
      unavailable: true,
    };
  }

  return request('/observability');
};

export { API_BASE_URL };
