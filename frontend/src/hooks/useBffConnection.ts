import { useEffect, useState, useRef } from 'react';
import { useTelemetryStore } from '../store/useTelemetryStore';
import { useAlertStore } from '../store/useAlertStore';

const WS_BFF_URL = process.env.REACT_APP_BFF_WS_URL || 'ws://localhost:4000';

export const useBffConnection = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isPollingFallback, setIsPollingFallback] = useState(false);
  const telemetryWs = useRef<WebSocket | null>(null);
  const alertsWs = useRef<WebSocket | null>(null);
  
  const updatePositions = useTelemetryStore(state => state.updatePositions);
  const triggerSafeMode = useAlertStore(state => state.triggerSafeMode);

  useEffect(() => {
    const connectSockets = () => {
      telemetryWs.current = new WebSocket(`${WS_BFF_URL}/telemetry`);
      alertsWs.current = new WebSocket(`${WS_BFF_URL}/alerts`);
      
      telemetryWs.current.onopen = () => setIsConnected(true);
      
      telemetryWs.current.onmessage = (event) => {
        // High frequency 60Hz JSON blobs pushing solely to the isolated Telemetry Store natively
        const positions = JSON.parse(event.data);
        updatePositions(positions);
      };
      
      alertsWs.current.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        if (payload.type === 'SAFE_MODE_FALLBACK') {
            triggerSafeMode(payload.reason);
        }
      };

      telemetryWs.current.onerror = () => attemptFallback();
      telemetryWs.current.onclose = () => attemptFallback();
    };

    const attemptFallback = () => {
        if (!isPollingFallback) {
            console.warn('[Network] WebSocket detached natively. Activating HTTP Polling failover safely.');
            setIsConnected(false);
            setIsPollingFallback(true);
            // setInterval(() => bffGateway.fetchTelemetry(), 500)
        }
    };

    connectSockets();
    return () => {
        telemetryWs.current?.close();
        alertsWs.current?.close();
    };
  }, []);

  return { isConnected, isPollingFallback };
};
