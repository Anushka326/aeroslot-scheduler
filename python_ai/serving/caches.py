from typing import Dict, Any, Optional

class FeatureCache:
    """Stores operational feature combinations minimizing repetitive extraction bounds."""
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        
    def get(self, flight_hash: str) -> Optional[Dict[str, Any]]:
        return self._cache.get(flight_hash)
        
    def set(self, flight_hash: str, features: Dict[str, Any]):
        self._cache[flight_hash] = features

class PredictionCache:
    """Stores the specific inference results ensuring immediate <5ms handoff on duplicate checks."""
    def __init__(self):
        self._cache: Dict[str, float] = {}
        
    def get(self, signature_hash: str) -> Optional[float]:
        return self._cache.get(signature_hash)
        
    def set(self, signature_hash: str, prediction: float):
        self._cache[signature_hash] = prediction
