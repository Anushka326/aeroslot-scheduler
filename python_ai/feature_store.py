import pandas as pd
from typing import List

class FeatureStore:
    """
    Centralized Feature Store ensuring absolute consistency 
    between Training, Validation, and Inference payloads.
    """
    def __init__(self):
        # Operational Features
        self.operational_features = [
            'taxi_queue_length', 
            'runway_occupancy_time', 
            'separation_req_seconds'
        ]
        # Graph Topology Features
        self.graph_features = [
            'conflict_degree', 
            'node_centrality'
        ]
        # Delay Propagation Features
        self.delay_features = [
            'previous_flight_delay', 
            'rolling_airport_delay_avg'
        ]
        
    def get_layer1_predictive_features(self) -> List[str]:
        """Features mapping to Delay and Congestion XGBoost Regression Models"""
        return self.operational_features + self.delay_features
        
    def get_layer2_decision_features(self) -> List[str]:
        """Features mapping to Priority & Runway Allocation Decision Classifiers"""
        # Decisions rely on the predictive outputs structurally alongside topological constraints
        return self.operational_features + self.graph_features + ['congestion_score_prediction']
        
    def validate_schema(self, df: pd.DataFrame, layer: int) -> bool:
        """Enforces schema consistency protecting the ML boundaries."""
        required = self.get_layer1_predictive_features() if layer == 1 else self.get_layer2_decision_features()
        missing = [f for f in required if f not in df.columns]
        if missing:
            raise ValueError(f"Feature Store Schema Violation! Missing: {missing}")
        return True
