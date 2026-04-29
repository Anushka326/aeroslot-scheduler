from db_config import get_connection

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS flights (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        flight_id varchar(20),
        airline varchar(50),
        mode varchar(20),
        aircraft_type varchar(30),
        wake_category varchar(20),
        origin_airport varchar(20),
        destination_airport varchar(20),
        eta_seconds int,
        priority_score float,
        emergency_flag tinyint(1),
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS predictions (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        flight_id varchar(20),
        predicted_delay int,
        conflict_risk float,
        priority_score float,
        timestamp timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS delay_predictions (
        prediction_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        flight_id varchar(20),
        predicted_delay float,
        congestion_risk float,
        recommended_runway varchar(20),
        model_used varchar(30),
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS runway_assignments (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        flight_id varchar(20),
        runway_id varchar(10),
        assigned_time int,
        delay int,
        timestamp timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS runway_schedule (
        schedule_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        flight_id varchar(20),
        runway varchar(20),
        assigned_slot datetime,
        algorithm_used varchar(50),
        status varchar(30),
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS history_logs (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        event_type varchar(50),
        event_msg text,
        timestamp timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS emergency_events (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        flight_id varchar(20),
        event_type varchar(50),
        action_taken text,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS algorithm_switches (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        switch_from varchar(50),
        switch_to varchar(50),
        reason text,
        timestamp timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS algorithm_switch_logs (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        old_algorithm varchar(50),
        new_algorithm varchar(50),
        reason text,
        switch_time timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """,
]


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    for statement in SCHEMA:
        cursor.execute(statement)
    conn.commit()
    cursor.close()
    conn.close()
    print("[MySQL] AeroSlot schema ready.")


if __name__ == "__main__":
    init_db()
