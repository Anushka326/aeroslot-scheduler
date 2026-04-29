import json
import logging
import os
from datetime import datetime

class AuditDecisionLogger:
    """
    Absolute Execution Audit Log.
    Tracks immutable variables determining every specific Runway Assignment physically 
    for explainability / regression bounds validation natively.
    """
    def __init__(self, log_path: str = "logs/audit_trail.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self.logger = logging.getLogger("DecisionAudit")

    def log_assignment_decision(self, flight_id: str, inputs: dict, ml_scores: dict, conflict_states: dict, override: bool = False):
        """
        Record the precise parameters executing an assignment.
        Critical for XAI Panel mappings and aviation-regulation structures.
        """
        record = {
            "timestamp_utc": datetime.utcnow().isoformat(),
            "flight_id": flight_id,
            "deterministic_inputs": inputs,
            "ml_heuristics": ml_scores,
            "conflict_checker_state": conflict_states,
            "is_emergency_override": override
        }
        
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(record) + '\n')
            
        self.logger.info(f"[AUDIT LOGGED] Runway locked for {flight_id}.")
