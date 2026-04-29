from db_config import get_connection, dict_rows
from init_db import init_db

init_db()

def save_flight(data):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO flights (
            flight_id, airline, mode, aircraft_type, wake_category, origin_airport,
            destination_airport, eta_seconds, taxi_time, runway_occupancy,
            requested_runway, priority_score, emergency_flag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("flight_id"),
            data.get("airline"),
            data.get("mode"),
            data.get("aircraft_type"),
            data.get("wake_category", data.get("wake", "Medium")),
            data.get("origin", data.get("origin_airport", "UNK")),
            data.get("destination", data.get("destination_airport", "UNK")),
            int(data.get("eta", data.get("eta_seconds", 0)) or 0),
            int(data.get("taxi_time", 0) or 0),
            int(data.get("runway_occupancy", 0) or 0),
            data.get("requested_runway", "AUTO"),
            float(data.get("priority", data.get("priority_score", 0)) or 0),
            int(bool(data.get("emergency", False))),
        ),
    )
    conn.commit()
    conn.close()

def save_prediction(data):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO delay_predictions
        (flight_id, predicted_delay, conflict_risk, priority_score, recommended_runway, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("flight_id", data.get("id")),
            float(data.get("predicted_delay", data.get("delay", 0)) or 0),
            float(data.get("conflict_risk", data.get("risk", 0)) or 0),
            float(data.get("priority_score", data.get("ml_score", data.get("score", 0))) or 0),
            data.get("recommended_runway", data.get("recommendedRunway", "AUTO")),
            float(data.get("confidence", 0) or 0),
        ),
    )
    conn.commit()
    conn.close()

def save_assignment(data, algorithm=None):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO schedule_results (flight_id, runway_id, slot_time, delay, status, algorithm)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("id", data.get("flight_id")),
            data.get("assignedRunway", data.get("assigned_runway", data.get("runway_id", "27L"))),
            int(data.get("slotTime", data.get("assigned_time", 0)) or 0),
            int(data.get("delay", 0) or 0),
            data.get("status", "SCHEDULED"),
            algorithm,
        ),
    )
    conn.commit()
    conn.close()

def save_runway_state(runway_id, state):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO runway_states
        (runway_id, status, assigned_aircraft, timer, wake_separation, utilization, queue_length)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            runway_id,
            state.get("status", "FREE"),
            state.get("assignedAC"),
            int(state.get("timer", 0) or 0),
            int(state.get("sep", 0) or 0),
            float(state.get("utilization", 0) or 0),
            int(state.get("queueLength", state.get("depth", 0)) or 0),
        ),
    )
    conn.commit()
    conn.close()

def save_switch(data):
    conn = get_connection()
    conn.execute(
        "INSERT INTO algorithm_switch_log (switch_from, switch_to, reason) VALUES (?, ?, ?)",
        (data.get("from"), data.get("to"), data.get("reason")),
    )
    conn.commit()
    conn.close()

def save_log(event_type, msg):
    conn = get_connection()
    conn.execute("INSERT INTO event_history (event_type, event_msg) VALUES (?, ?)", (event_type, msg))
    conn.commit()
    conn.close()

def save_emergency(data):
    conn = get_connection()
    conn.execute(
        "INSERT INTO emergencies (flight_id, emergency_type, severity) VALUES (?, ?, ?)",
        (data.get("flight_id"), data.get("emergency_type", "Emergency"), data.get("severity", "HIGH")),
    )
    conn.commit()
    conn.close()

def get_history():
    conn = get_connection()
    cursor = conn.execute("SELECT id, event_type, event_msg, timestamp FROM event_history ORDER BY timestamp DESC LIMIT 200")
    rows = dict_rows(cursor)
    conn.close()
    return rows

def get_archive():
    conn = get_connection()
    archive = {}
    for key, sql in {
        "flights": "SELECT * FROM flights ORDER BY created_at DESC LIMIT 200",
        "schedule_results": "SELECT * FROM schedule_results ORDER BY created_at DESC LIMIT 200",
        "delay_predictions": "SELECT * FROM delay_predictions ORDER BY created_at DESC LIMIT 200",
        "algorithm_switch_log": "SELECT * FROM algorithm_switch_log ORDER BY created_at DESC LIMIT 200",
        "runway_states": "SELECT * FROM runway_states ORDER BY created_at DESC LIMIT 200",
        "event_history": "SELECT * FROM event_history ORDER BY timestamp DESC LIMIT 200",
        "emergencies": "SELECT * FROM emergencies ORDER BY created_at DESC LIMIT 200",
    }.items():
        archive[key] = dict_rows(conn.execute(sql))
    conn.close()
    return archive

def clear_db():
    conn = get_connection()
    for table in ["flights", "schedule_results", "delay_predictions", "algorithm_switch_log", "runway_states", "event_history", "emergencies"]:
        conn.execute(f"DELETE FROM {table}")
    conn.commit()
    conn.close()
