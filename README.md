# AeroSlot Scheduler: Smart AI-Based Airport Runway Scheduler

**AeroSlot Scheduler** is a research-grade intelligent airport control tower simulator and runway optimization platform. It combines a high-performance C++ scheduling engine with a Python-based Machine Learning inference layer and an interactive React frontend dashboard. The system simulates and optimizes real-world airport operations for both landing and takeoff sequencing, balancing safety, throughput, delay reduction, conflict avoidance, and emergency handling.

---

## ✈️ Key Features

- **Multi-Algorithm Scheduling Engine (C++)**: Supports FCFS (Baseline), Priority Scheduling (based on fuel, emergencies), Preemptive Emergency Scheduling, and Min-Delay Greedy Scheduling.
- **AI-Powered Delay Prediction (Python/ML)**: Uses pre-trained Random Forest and XGBoost models to predict flight delays, congestion risks, and runway occupancies based on historical data.
- **Conflict Graph Detection**: Implements graph theory to detect and prevent runway conflicts based on wake turbulence separation and occupancy times.
- **Interactive Control-Tower Dashboard (React)**: A highly visual, glassmorphism-themed frontend for monitoring flights, submitting requests, analyzing delay data, and triggering what-if simulation scenarios.
- **Digital Twin Coordinates**: Dynamic (X, Y) positioning mapping for aircraft visualization.
- **Data Persistence**: MySQL database backend for logging tactical audits and schedule histories.

---

## 🏗️ Architecture & Technology Stack

The project follows a microservices-style architecture divided into three main components:

1. **Frontend (`/frontend`)**: 
   - **Tech**: React, Tailwind CSS, Vite.
   - **Role**: Provides the interactive dashboard, flight input forms, analytics charts, and simulation controls.

2. **Core Scheduling Engine (`/cpp_scheduler`)**:
   - **Tech**: Modern C++ (OOP).
   - **Role**: Acts as the central scheduler, using priority queues, heaps, and conflict graphs to handle real-time runway assignments and emergency preemptions.

3. **AI/ML Inference Layer (`/python_ai`)**:
   - **Tech**: Python, Flask, `scikit-learn`, `joblib`.
   - **Role**: Exposes a REST API for the frontend and C++ engine to query machine learning models for delay predictions and priority scoring.

4. **Datasets (`/Datasets`)**:
   - Fuses data from OpenSky Network, Amelia-48, NOAA Weather Data, and FAA Delay Data to train the machine learning models.

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** & **npm** (for the frontend)
- **Python 3.8+** (for the ML backend)
- **C++ Compiler** & **CMake** (for building the C++ scheduler engine)
- **MySQL** (for database operations)

### Installation & Execution

The project comes with an orchestrator script to launch the entire system seamlessly.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anushka326/aeroslot-scheduler.git
   cd aeroslot-scheduler
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r python_ai/requirements.txt
   ```
   *(Ensure you have your virtual environment activated if you use one)*

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

## 📊 System Inference Parameters

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

## 🛡️ License

This project is built for research, simulation, and capstone purposes.
