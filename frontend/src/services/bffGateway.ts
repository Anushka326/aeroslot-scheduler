import axios from 'axios';

const BFF_BASE_URL = process.env.REACT_APP_BFF_URL || 'http://localhost:4000/api';

/**
 * The Backend For Frontend (BFF) Orchestration Gateway.
 * The React UI NEVER interfaces directly with C++ engines or Python API models independently.
 */
export const bffGateway = {
  // Command & State Control (Routes down to C++)
  fetchRunwayLocks: async () => {
    return await axios.get(`${BFF_BASE_URL}/engine/runways`);
  },
  
  commitScenario: async (scenarioData: any) => {
    return await axios.post(`${BFF_BASE_URL}/engine/scenario`, scenarioData);
  },

  // Advisory Interactions (Routes down to Python MLOps Layer)
  fetchDelayPrediction: async (flightId: string, features: any) => {
    return await axios.post(`${BFF_BASE_URL}/ai/predict-delay`, { flightId, ...features });
  },
  
  fetchHealthChecks: async () => {
    return await axios.get(`${BFF_BASE_URL}/health`); // Returns metrics combining C++ & Python drift states safely
  }
};
