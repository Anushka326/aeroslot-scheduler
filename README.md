# AeroSlot Scheduler: Smart AI-Based Airport Runway Scheduling & Air Traffic Optimization System

**AeroSlot Scheduler** is a research-grade intelligent airport control tower simulator and runway optimization platform. It combines a high-performance C++ scheduling engine with a Python-based Machine Learning inference layer and an interactive React frontend dashboard. The system simulates and optimizes real-world airport operations for both landing and takeoff sequencing, balancing safety, throughput, delay reduction, conflict avoidance, and emergency handling.

---

## ✈️ Problem Statement

Traditional runway scheduling struggles under growing air traffic complexity due to:
- **Flight Delays & Congestion**: Cascading delays, departure queues, and missed slots.
- **Inefficient Runway Utilization**: Poorly balanced operations across runways.
- **Static / Manual Scheduling**: Reliance on First-Come-First-Serve (FCFS) sequencing and reactive decision-making.
- **Poor Emergency Handling**: Disrupted normal schedules and reduced throughput.
- **Lack of Predictive Intelligence**: Missing proactive delay prediction and slot optimization.
- **No Adaptive Scheduling**: Struggling during critical weather conditions and simultaneous emergencies.

## 🚀 Proposed Solution

An AI-assisted runway scheduling system that combines prediction, optimization, safety constraints, and real-time control:
- **Intelligent Flight Scheduling**: Dynamically schedules and allocates optimal runway slots.
- **AI/ML Delay Prediction**: Predicts delays before congestion escalates using ML models.
- **Hybrid Adaptive Scheduling Engine**: Automatically switches algorithms based on traffic (FCFS, Greedy Min Delay, Preemptive, Priority).
- **Conflict-Aware Safe Scheduling**: Wake turbulence separation and dynamic safety buffers.

---

## 📐 Core Scheduling Intelligence Formulas

The system relies on multi-objective optimization to balance delay, fuel, and risk.

**1. Optimization Objective**
Minimize: `J = α(Delay) + β(ConflictRisk) − γ(Throughput)`
*(Goal: Reduce Delay and Conflict Risk while increasing Throughput)*

**2. Priority Scoring**
Ranks urgency for the Priority Scheduler:
`Priority = Emergency + (Fuel × 9) + Passenger + Cargo`

**3. Delay Prediction**
Predicts operational delay before runway allocation:
`Delay = max(5, Base + Congestion + Weather − Urgency)`

**4. Slot Time Allocation**
Determines the safest optimal slot time:
`SlotTime = max(ETA, RunwayLoad + Separation)`

**5. Runway Allocation Delay**
`AllocationDelay = max(0, SlotTime − ETA) + RiskBuffer`

**6. Conflict Risk & Detection**
Prevents runway overlap conflicts. For any two aircraft sequences (s1, e1) and (s2, e2):
`max(s1, s2) < min(e1, e2)`
Conflict Risk Calculation: `Risk = f(Delay, Congestion, Emergency)`
Conflict Score: `ConflictScore = Risk × 100`

**7. Safety KPI**
`Safety = 100 − RiskPenalty`

---

## 🏗️ System Architecture & Technology Stack

The project follows a microservices-style architecture:

### 1. Frontend (`/frontend`)
- **Tech Stack**: React, Tailwind CSS, Recharts, D3.js, Three.js (Digital Twin visualizer).
- **Role**: Provides the interactive dashboard, flight input forms, analytics charts, and simulation controls.

### 2. Core Scheduling Engine (`/cpp_scheduler`)
- **Tech Stack**: Modern C++ (OOP, DSA).
- **Algorithms**: FCFS, Priority, Preemptive, Greedy, Conflict Graph.
- **Role**: Acts as the central scheduler, using priority queues, heaps, and conflict graphs to handle real-time runway assignments and emergency preemptions.

### 3. AI/ML Inference Layer (`/python_ai`)
- **Tech Stack**: Python, Flask, Scikit-learn, XGBoost.
- **Models**: Random Forest, XGBoost.
- **Role**: Exposes a REST API for predicting flight delays, congestion risks, and runway occupancies based on historical data.

### 4. Database
- **Tech Stack**: MySQL
- **Role**: Persistence for Tactical Audit Logs and Schedule History.

---

## 📊 Datasets and Data Fusion Pipeline

The ML models are trained on a Merged Aviation Intelligence Dataset combined from four primary sources:

1. **OpenSky State Vectors (2017–2022)**: Trajectory data, arrivals, departures, congestion patterns.
2. **OpenSky Aircraft Metadata (2021–2025)**: Aircraft types, wake turbulence categories for separation constraints.
3. **Amelia-48 / Amelia Mini Dataset (2024)**: Airport surface movement, taxi movement, runway occupancy behavior.
4. **Historical Flight Delay Datasets (FAA/BTS/Kaggle)**: Supervised learning dataset capturing historical delay patterns and causes.

**Data Fusion Flow:**
`OpenSky Trajectories + Aircraft Metadata + Amelia Surface Operations + Historical Delay Data` 
➡️ `Merged Aviation Intelligence Dataset`
➡️ `ML Models + C++ Scheduling Engine`

---

## ⚙️ Getting Started

### Prerequisites
- **Node.js** & **npm** (for the frontend)
- **Python 3.8+** (for the ML backend)
- **C++ Compiler** & **CMake** (for building the C++ scheduler engine)
- **MySQL** (for database operations)

### Installation & Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anushka326/aeroslot-scheduler.git
   cd aeroslot-scheduler
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r python_ai/requirements.txt
   ```

3. **Install Frontend Dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Build the C++ Scheduler**:
   Navigate to `/cpp_scheduler` and use CMake to build the executable into the `build/Debug/` directory.

5. **Launch the System**:
   You can run all microservices at once using the provided Python orchestrator script:
   ```bash
   python launch_system.py
   ```
   *This script boots the Python ML Inference service (Port 4000), the C++ Scheduler Engine, and the React UI Dashboard.*

---

## 🚦 System Inference Parameters

When submitting a flight via the dashboard, the system processes several parameters:

| Parameter | Description |
| :--- | :--- |
| **Call Sign** | ICAO/IATA identifier (e.g. `DL452`) |
| **Operation Mode** | `LANDING` or `TAKEOFF` |
| **Frame Type** | Aircraft model (e.g. `B747`, `A350`) |
| **Wake Class** | `HEAVY`, `MEDIUM`, or `LIGHT` (determines separation requirements) |
| **ETA** | Estimated time of arrival (in seconds) |
| **Fuel Criticality** | Scale 1 (Nominal) to 10 (Critical) |
| **Occupancy** | Expected runway residency time in seconds |

## 🛡️ Scope & Limitations

**Scope**: Smart Single-Airport Runway Optimization, Real-Time Intelligent Scheduling, Delay Prediction & Decision Support, Future Multi-Airport Network Scheduling, Digital Twin Expansion.

**Limitations**: Currently focused on single-airport optimizations; ML accuracy heavily depends on underlying prototype-scale dataset quality.

## 📝 License
This project is built for research, simulation, and capstone purposes.
