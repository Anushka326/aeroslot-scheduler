from db_config import get_connection

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_id TEXT NOT NULL,
        airline TEXT,
        mode TEXT,
        aircraft_type TEXT,
        wake_category TEXT,
        origin_airport TEXT,
        destination_airport TEXT,
        eta_seconds INTEGER,
        taxi_time INTEGER,
        runway_occupancy INTEGER,
        requested_runway TEXT,
        priority_score REAL,
        emergency_flag INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS schedule_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_id TEXT,
        runway_id TEXT,
        slot_time INTEGER,
        delay INTEGER,
        status TEXT,
        algorithm TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS delay_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_id TEXT,
        predicted_delay REAL,
        conflict_risk REAL,
        priority_score REAL,
        recommended_runway TEXT,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS algorithm_switch_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        switch_from TEXT,
        switch_to TEXT,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS runway_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        runway_id TEXT,
        status TEXT,
        assigned_aircraft TEXT,
        timer INTEGER,
        wake_separation INTEGER,
        utilization REAL,
        queue_length INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS event_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        event_msg TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS emergencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_id TEXT,
        emergency_type TEXT,
        severity TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
]

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    for statement in SCHEMA:
        cursor.execute(statement)
    conn.commit()
    conn.close()
    print("[SQLite] AeroSlot schema initialized.")

if __name__ == "__main__":
    init_db()
