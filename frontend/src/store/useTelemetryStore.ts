import { create } from 'zustand';
import { AircraftLocation } from '../types/telemetry';

interface TelemetryState {
  aircraftPositions: Record<string, AircraftLocation>;
  lastUpdateTimestamp: number;
  updatePositions: (newPositions: Record<string, AircraftLocation>) => void;
  clearTelemetry: () => void;
}

export const useTelemetryStore = create<TelemetryState>((set) => ({
  aircraftPositions: {},
  lastUpdateTimestamp: 0,
  
  // Natively bounded to ignore heavy reconciliations globally during the 60Hz C++ streams
  updatePositions: (newPositions) => set((state) => ({
    aircraftPositions: { ...state.aircraftPositions, ...newPositions },
    lastUpdateTimestamp: Date.now()
  })),
  
  clearTelemetry: () => set({ aircraftPositions: {}, lastUpdateTimestamp: 0 })
}));
