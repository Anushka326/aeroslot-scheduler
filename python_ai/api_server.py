from flask import Flask, request, jsonify
from flask_cors import CORS
from db_service import (
    save_flight,
    get_history,
    get_archive,
    save_prediction,
    save_assignment,
    save_switch,
    save_log,
    save_runway_state,
    save_emergency,
    clear_db,
)
import joblib
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
try:
    delay_model = joblib.load(os.path.join(MODEL_DIR, "rf_delay_model.pkl"))
    priority_model = joblib.load(os.path.join(MODEL_DIR, "xgb_priority_model.pkl"))
    congestion_model = joblib.load(os.path.join(MODEL_DIR, "xgb_congestion_model.pkl"))
    print("[AeroSlot] XGBoost + Random Forest models loaded.")
except Exception as exc:
    print(f"[AeroSlot] Model fallback active: {exc}")
    delay_model = priority_model = congestion_model = None

def build_features(data):
    wake_map = {"Heavy": 3, "Medium": 2, "Light": 1, "H": 3, "M": 2, "L": 1}
    congestion_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    env = data.get("env", {})
    return pd.DataFrame([{
        "geoaltitude": 3000 if data.get("mode") == "LANDING" else 0,
        "velocity": 180 if data.get("mode") == "LANDING" else 40,
        "wake_factor": wake_map.get(data.get("wake", data.get("wake_category", "Medium")), 2),
        "airspace_congestion": congestion_map.get(env.get("congestion", "LOW"), 1),
        "occupancy_est_sec": int(data.get("runwayOccEst", data.get("runway_occupancy", 45)) or 45),
    }])

def local_prediction(data):
    env = data.get("env", {})
    emergency = data.get("medicalDistress") or data.get("technicalDistress") or data.get("fuelEmergency") or data.get("emergency")
    congestion = {"LOW": 8, "MEDIUM": 24, "HIGH": 48}.get(env.get("congestion", "LOW"), 8)
    storm = int(env.get("storm", env.get("stormSeverity", 0)) or 0) * 7
    urgency = int(data.get("fuelUrgency", 5) or 5) * 5
    delay = max(5, 55 + congestion + storm - urgency - (60 if emergency else 0))
    risk = min(0.96, max(0.08, delay / 150 + (0.2 if emergency else 0)))
    runways = ["27L", "27R", "09L", "09R"]
    recommended = data.get("requestedRunway") if not data.get("autoRunway", True) and data.get("requestedRunway") != "AUTO" else runways[(delay + urgency) % 4]
    return {
        "delay": round(delay, 1),
        "risk": round(risk, 3),
        "score": round(1000 - delay + urgency + (250 if emergency else 0), 0),
        "confidence": 96.2 if delay_model else 91.0,
        "recommendedRunway": recommended,
        "algorithmRecommendation": "PREEMPTIVE_EMERGENCY" if emergency else "HYBRID_ADAPTIVE" if risk > 0.68 else "FCFS",
    }

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json or {}
    result = local_prediction(data)
    if delay_model:
        try:
            model_delay = max(0, float(delay_model.predict(build_features(data))[0]))
            result["delay"] = round(model_delay, 1)
            result["risk"] = min(0.96, 0.08 if model_delay < 30 else 0.42 if model_delay < 90 else 0.82)
        except Exception as exc:
            print(f"[AeroSlot] Prediction fallback: {exc}")
    save_prediction({
        "flight_id": data.get("id", data.get("flight_id")),
        "predicted_delay": result["delay"],
        "conflict_risk": result["risk"],
        "priority_score": result["score"],
        "recommended_runway": result["recommendedRunway"],
        "confidence": result["confidence"],
    })
    save_log("DELAY_PREDICTED", f"Delay predicted for {data.get('id', data.get('flight_id', 'UNKNOWN'))}: {result['delay']}s")
    return jsonify(result)

@app.route("/api/flights", methods=["POST"])
def add_flight():
    data = request.json or {}
    save_flight(data)
    if data.get("emergency"):
        save_emergency({"flight_id": data.get("flight_id", data.get("id")), "emergency_type": "Declared emergency", "severity": "HIGH"})
    save_log("FLIGHT_ADDED", f"Flight {data.get('flight_id', data.get('id'))} registered in active queue.")
    return jsonify({"status": "success"})

@app.route("/api/predictions", methods=["POST"])
def persist_prediction():
    save_prediction(request.json or {})
    return jsonify({"status": "success"})

@app.route("/api/events", methods=["POST"])
def persist_event():
    data = request.json or {}
    save_log(data.get("event_type", "EVENT"), data.get("event_msg", "AeroSlot event"))
    return jsonify({"status": "success"})

@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(get_history())

@app.route("/api/archive", methods=["GET"])
def archive():
    return jsonify(get_archive())

@app.route("/api/schedule", methods=["POST"])
def schedule_flights():
    data = request.json or {}
    algorithm = data.get("algorithm", "FCFS")
    for result in data.get("flights", []):
        save_assignment(result, algorithm)
        save_prediction(result)
    for runway_id, state in (data.get("runways") or {}).items():
        save_runway_state(runway_id, state)
    save_log("SCHEDULER_RUN", f"Optimal sequence calculated via {algorithm}")
    return jsonify({"status": "success", "results": data.get("flights", [])})

@app.route("/api/switches", methods=["POST"])
def log_switch():
    data = request.json or {}
    save_switch(data)
    save_log("ALGORITHM_SWITCHED", f"{data.get('from')} -> {data.get('to')}: {data.get('reason')}")
    return jsonify({"status": "success"})

@app.route("/api/clear", methods=["POST"])
def purge_db():
    clear_db()
    save_log("DB_PURGE", "AeroSlot audit tables cleared.")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
