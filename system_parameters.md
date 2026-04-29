# AeroSlot Scheduler: System Operational Parameters

This document outlines the input and output paradigms for the **AeroSlot Intelligent Runway Optimizer**.

## 1. System Inputs (Inference Parameters)
When registering a flight via the **AeroSlot Submission Deck**, the following parameters are processed by the **Python Random Forest Backend**:

| Parameter | Type | Domain / Values | Impact |
| :--- | :--- | :--- | :--- |
| **Call Sign** | String | ICAO/IATA (e.g. `DL452`) | Data Persistence Key |
| **Operation Mode** | Enum | `LANDING` / `TAKEOFF` | Feature Vector Altitude/Velocity |
| **Frame Type** | Searchable | `B747`, `A350`, `B737`, etc. | Wake Turbulence Class |
| **Wake Class** | Enum | `HEAVY` (H), `MEDIUM` (M), `LIGHT` (L) | Minimum Separation Requirements |
| **ETA (S)** | Integer | 0 - 3600 (Seconds from active) | Temporal Slot Selection |
| **Fuel Criticality** | Scale | 1 (Nominal) - 10 (Critical) | Priority Weighting |
| **Occupancy (S)** | Integer | 30 - 120 (Seconds) | Runway Thread Residency |
| **Pax/Cargo Priority** | Categories | VIP, MedEvac, Dangerous Goods | Conflict Resolution Weighting |

## 2. System Outputs (Intelligence Feedback)
The **AeroSlot ML Engine** returns the following tactical telemetry:

- **Predicted Delay (S)**: Real-time inference from `rf_delay_model.pkl` predicting touchdown latency.
- **Conflict Risk (%)**: Probability of separation violation based on current sector density.
- **Priority Score**: Weighted numerical value (0-1000) used for the **Adaptive Scheduler** queue position.
- **AI Confidence (%)**: Quantified certainty of the XGBoost/RF prediction.
- **Digital Twin Coordinates**: Dynamic (X,Y) positioning for aircraft visualization on the terminal map.

## 3. Technology Stack & Dataset Integration
- **Frontend**: React + Tailwind + AeroSlot Glassmorphism Theme.
- **Backend Intelligence**: Flask API (Python) using `scikit-learn` and `joblib`.
- **Database**: MySQL persistence for Tactical Audit Logs and Schedule History.
- **Datasets**: Using the **Master Records** (`master_records.parquet`) merged from:
    - **OpenSky Network**: Real-world aircraft trajectory states.
    - **Amelia Dashboard**: Historical flight performance data.
    - **Aviation Metadata**: Detailed airframe specific constraints (Wake/Size).

## 4. How to Test the System
1. Ensure the **Aeroslot Backend** is running (`python python_ai/api_server.py`).
2. Ensure the **React Frontend** is running (`npm run dev`).
3. **Add a Flight**: Enter a `B747` with high Fuel Criticality.
4. **Observe Inference**: Notice the **Predicted Delay** card populating via real Python backend call.
5. **Optimize**: Click **Launch AeroSlot Optimization** to synchronize the Digital Twin map and Runway Status cards.
