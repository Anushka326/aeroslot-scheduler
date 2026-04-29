import logging
from typing import Dict, Any

class TelemetryLogger:
    """
    Centralized Observability Module.
    Tracks ML inferences, latencies, and health checks natively structured 
    for future Prometheus / Grafana dashboards.
    """
    def __init__(self):
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        self.logger = logging.getLogger("MLOps-Telemetry")

    def log_inference(self, flight_id: str, confidence: float, latency_ms: float):
        self.logger.info(f"[Inference] Flight: {flight_id} | Confidence: {confidence:.2f} | Latency: {latency_ms:.1f}ms")
        
    def log_drift_warning(self, feature: str, severity: str):
        """ Severity: Green, Yellow (Retrain Proposal), Red (Critical) """
        if severity == "RED":
            self.logger.error(f"[Drift Alert] RED severity on {feature}. Suggesting Safe-Mode evaluation.")
        elif severity == "YELLOW":
            self.logger.warning(f"[Drift Warn] YELLOW severity on {feature}. Retraining Proposal Generated.")
            
    def health_check(self) -> Dict[str, Any]:
        """Provides basic liveness probes securely."""
        return {"status": "healthy", "service": "python_ai_mlops"}
