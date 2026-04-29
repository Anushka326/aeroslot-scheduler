from datetime import datetime, timedelta

from db_config import dict_rows, get_connection
from init_db import init_db

init_db()


def _execute(sql, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    cursor.close()
    conn.close()


def _query(sql, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = dict_rows(cursor)
    cursor.close()
    conn.close()
    return rows


def _flight_id(data):
    return data.get("flight_id") or data.get("id") or data.get("flightId")


def _assigned_slot(data):
    raw_slot = data.get("assigned_slot") or data.get("assignedSlot")
    if raw_slot:
        return raw_slot
    seconds = int(data.get("slotTime", data.get("assigned_time", 0)) or 0)
    return datetime.now() + timedelta(seconds=seconds)


def save_flight(data):
    _execute(
        """
        INSERT INTO flights (
            flight_id, airline, mode, aircraft_type, wake_category, origin_airport,
            destination_airport, eta_seconds, priority_score, emergency_flag
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            _flight_id(data),
            data.get("airline"),
            data.get("mode"),
            data.get("aircraft_type", data.get("type")),
            data.get("wake_category", data.get("wake", "Medium")),
            data.get("origin", data.get("origin_airport", "UNK")),
            data.get("destination", data.get("dest", data.get("destination_airport", "UNK"))),
            int(data.get("eta", data.get("eta_seconds", 0)) or 0),
            float(data.get("priority", data.get("priority_score", 0)) or 0),
            int(bool(data.get("emergency", data.get("emergency_flag", False)))),
        ),
    )


def save_prediction(data):
    flight_id = _flight_id(data)
    predicted_delay = float(data.get("predicted_delay", data.get("delay", 0)) or 0)
    conflict_risk = float(data.get("conflict_risk", data.get("risk", data.get("congestion_risk", 0))) or 0)
    priority_score = float(data.get("priority_score", data.get("ml_score", data.get("score", data.get("priority", 0)))) or 0)
    recommended_runway = data.get("recommended_runway", data.get("recommendedRunway", data.get("assignedRunway", "AUTO")))
    model_used = data.get("model_used", data.get("model", "AeroSlot scheduler"))[:30]

    _execute(
        """
        INSERT INTO predictions (flight_id, predicted_delay, conflict_risk, priority_score)
        VALUES (%s, %s, %s, %s)
        """,
        (flight_id, int(round(predicted_delay)), conflict_risk, priority_score),
    )
    _execute(
        """
        INSERT INTO delay_predictions
        (flight_id, predicted_delay, congestion_risk, recommended_runway, model_used)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (flight_id, predicted_delay, conflict_risk, recommended_runway, model_used),
    )


def save_assignment(data, algorithm=None):
    flight_id = _flight_id(data)
    runway = data.get("assignedRunway", data.get("assigned_runway", data.get("runway_id", "27L")))
    assigned_time = int(data.get("slotTime", data.get("assigned_time", 0)) or 0)
    delay = int(data.get("delay", 0) or 0)

    _execute(
        """
        INSERT INTO runway_assignments (flight_id, runway_id, assigned_time, delay)
        VALUES (%s, %s, %s, %s)
        """,
        (flight_id, runway, assigned_time, delay),
    )
    _execute(
        """
        INSERT INTO runway_schedule
        (flight_id, runway, assigned_slot, algorithm_used, status)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (flight_id, runway, _assigned_slot(data), algorithm, data.get("status", "SCHEDULED")),
    )


def save_runway_state(runway_id, state):
    queue = state.get("queue") or []
    for index, flight in enumerate(queue):
        _execute(
            """
            INSERT INTO runway_schedule
            (flight_id, runway, assigned_slot, algorithm_used, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                _flight_id(flight),
                runway_id,
                datetime.now() + timedelta(seconds=index * int(flight.get("occupancy", 45) or 45)),
                "RUNWAY_STATE",
                state.get("status", "SCHEDULED"),
            ),
        )


def save_switch(data):
    old_algorithm = data.get("from", data.get("old_algorithm", data.get("switch_from")))
    new_algorithm = data.get("to", data.get("new_algorithm", data.get("switch_to")))
    reason = data.get("reason")

    _execute(
        "INSERT INTO algorithm_switches (switch_from, switch_to, reason) VALUES (%s, %s, %s)",
        (old_algorithm, new_algorithm, reason),
    )
    _execute(
        "INSERT INTO algorithm_switch_logs (old_algorithm, new_algorithm, reason) VALUES (%s, %s, %s)",
        (old_algorithm, new_algorithm, reason),
    )


def save_log(event_type, msg):
    _execute(
        "INSERT INTO history_logs (event_type, event_msg) VALUES (%s, %s)",
        (event_type, msg),
    )


def save_emergency(data):
    _execute(
        "INSERT INTO emergency_events (flight_id, event_type, action_taken) VALUES (%s, %s, %s)",
        (
            _flight_id(data),
            data.get("event_type", data.get("emergency_type", "Emergency")),
            data.get("action_taken", data.get("severity", "Emergency priority applied")),
        ),
    )


def get_history():
    return _query(
        "SELECT id, event_type, event_msg, timestamp FROM history_logs ORDER BY timestamp DESC LIMIT 200"
    )


def get_archive():
    archive = {}
    queries = {
        "flights": "SELECT * FROM flights ORDER BY created_at DESC LIMIT 200",
        "predictions": "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 200",
        "delay_predictions": "SELECT * FROM delay_predictions ORDER BY created_at DESC LIMIT 200",
        "runway_assignments": "SELECT * FROM runway_assignments ORDER BY timestamp DESC LIMIT 200",
        "runway_schedule": "SELECT * FROM runway_schedule ORDER BY created_at DESC LIMIT 200",
        "algorithm_switches": "SELECT * FROM algorithm_switches ORDER BY timestamp DESC LIMIT 200",
        "algorithm_switch_logs": "SELECT * FROM algorithm_switch_logs ORDER BY switch_time DESC LIMIT 200",
        "history_logs": "SELECT * FROM history_logs ORDER BY timestamp DESC LIMIT 200",
        "emergency_events": "SELECT * FROM emergency_events ORDER BY created_at DESC LIMIT 200",
    }
    for key, sql in queries.items():
        archive[key] = _query(sql)
    return archive


def clear_db():
    conn = get_connection()
    cursor = conn.cursor()
    for table in [
        "runway_schedule",
        "runway_assignments",
        "delay_predictions",
        "predictions",
        "algorithm_switch_logs",
        "algorithm_switches",
        "history_logs",
        "emergency_events",
        "flights",
    ]:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    cursor.close()
    conn.close()
