const API_BASE_URL =
  "https://aegis-autonomous-multimodal-world.onrender.com/api";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      errorText || `API request failed: ${response.status}`
    );
  }

  return response.json();
}

export async function getHealth() {
  return fetch(
    "https://aegis-autonomous-multimodal-world.onrender.com/health"
  ).then(async (response) => {
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return response.json();
  });
}

export async function runAutonomousCycle(payload) {
  return request("/autonomous/run", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getAutonomousResult() {
  return request("/autonomous/result");
}

export async function getObservationStatus() {
  return request("/observation-loop/status");
}

export async function getLatestWorldState() {
  return request("/observation-loop/world-state");
}

export async function getUncertaintyResult() {
  return request("/uncertainty/result");
}

export async function getVisionLanguageResult() {
  return request("/vision-language/result");
}

export async function getReplanningResult() {
  return request("/replanning/result");
}

export async function getVerificationHistory() {
  return request("/verification/history");
}

export default {
  getHealth,
  runAutonomousCycle,
  getAutonomousResult,
  getObservationStatus,
  getLatestWorldState,
  getUncertaintyResult,
  getVisionLanguageResult,
  getReplanningResult,
  getVerificationHistory,
};